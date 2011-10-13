from django.db import models
from akismet.akismet import Akismet
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.comments.moderation import CommentModerator
from django.contrib.comments.models import Comment
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.template import loader
import re

class MaybeLessSpamCommentModerator(CommentModerator):
	enable_field='enable_comments'
	email_notification = settings.COMMENT_EMAIL_NOTIFICATION_FLAG

	# After 30 days, force moderation
	auto_moderate_field = 'pub_date'
	moderate_after = settings.COMMENT_MODERATE_AFTER

	# After 60 days, force closure of comments
	auto_close_field = 'pub_date'
	close_after = settings.COMMENT_CLOSE_AFTER


	def moderate(self,comment,content_object,request):
		# return True means "moderated", i.e. mark non-public. 
		# return False means not "moderated", i.e. let through and the public can now see it. 

		# For now, assume that this is not akismet spam.
		comment.is_akismet_spam = False

		already_moderated = super(MaybeLessSpamCommentModerator,self).moderate(comment,content_object,request)
		if already_moderated:
			return True

		comment_string = comment.comment
		comment_string=comment_string.replace('\n', ' ')
		comment_string=comment_string.replace('\r', ' ')
		comment_string=" " + comment_string + " "


		bad_words_file_name = settings.BAD_WORDS_FILE
		bad_words_template = loader.get_template(bad_words_file_name)
		bad_words_string = bad_words_template.nodelist[0].render('')

		# Remove \n's from bad_words_string string
		bad_words_string=re.sub('\n','',bad_words_string)
		bad_words_re = re.compile(bad_words_string, re.IGNORECASE) 

		if bad_words_re.search(comment_string):
			return True

		the_current_domain = Site.objects.get_current().domain
		the_project_url="http://%s" % the_current_domain

		akismet_api = Akismet(settings.AKISMET_API_KEY, the_project_url)
		if akismet_api.verify_key():
			comment_author = request.REQUEST["name"]
			placeholder_comment_email = "r@r.com" # this forces Akimset to be more conservative

			akismet_data = {'blog':the_project_url, 'comment_type': 'comment', 'referrer':request.META['HTTP_REFERER'],'user_ip':comment.ip_address, 'user_agent':request.META['HTTP_USER_AGENT'], 'comment_author':comment_author, 'comment_author_email':placeholder_comment_email}

			akismet_response = akismet_api.comment_check(smart_str(comment_string), data=akismet_data,build_data=True)

			comment.is_akismet_spam = akismet_response
			return akismet_response

		# If reached here, the Akismet API has failed to verify the key, so to be safe, assume that this *IS* spam.
		comment.is_akismet_spam = True
		return True		

	def email(self, comment, content_object, request):
		# Only send email notifications is not akismet spam
		if not comment.is_akismet_spam:
			return super(MaybeLessSpamCommentModerator,self).email(comment, content_object, request)


	








