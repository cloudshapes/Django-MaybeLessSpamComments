from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
import datetime


class Model2(models.Model):
    title = models.CharField(max_length=50,help_text="title - max length 50 characters")
    fieldmodel2 = models.CharField(max_length=50,help_text="fieldmodel2 - max length 50 characters")
    pub_date = models.DateTimeField('date published')

    enable_comments = models.BooleanField(default=True)

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'

    def __unicode__(self):
        return self.title



# Register MaybeLessSpamCommentModerator moderator for Model2
from django.contrib.comments.moderation import moderator
from maybelessspamcomment.moderation import MaybeLessSpamCommentModerator
moderator.register(Model2, MaybeLessSpamCommentModerator)




