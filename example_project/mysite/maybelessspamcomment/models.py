from django.db import models
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings


class MaybeLessSpamComment(Comment):
    is_akismet_spam = models.BooleanField(_('is akismet spam'), default=False,
                    help_text=_('Indicates whether the content has been marked as spam by akismet or not.'))

    def get_absolute_url(self):
        return self.get_content_object_url()

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.user_name, ## changed this ever so slightly - didn't want the main logged in user, just the commenting person. 
            'date': self.submit_date,
            'comment': self.comment,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d






