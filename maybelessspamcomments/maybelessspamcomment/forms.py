from django import forms
from django.contrib.comments.forms import CommentForm
from maybelessspamcomment.models import MaybeLessSpamComment
from django.utils.translation import ungettext, ugettext_lazy as _
from django.conf import settings
from recaptcha_django import ReCaptchaWidget, ReCaptchaField



class MaybeLessSpamCommentForm(CommentForm):
    name          = forms.CharField(label=_("Name:"),  widget=forms.TextInput(attrs={'class':'comment_form_class'}),max_length=50, required=True)
    email         = forms.EmailField(widget=forms.HiddenInput,required=False)
    url           = forms.URLField(widget=forms.HiddenInput,required=False)
    comment       = forms.CharField(label=_('Comment:'), widget=forms.Textarea(attrs={'rows':'3', 'cols':'40', 'class':'comment_form_class'}), 	    max_length=settings.MAX_COMMENT_LENGTH, required=True)
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(attrs={'theme':'custom', 'custom_theme_widget':'recaptcha_widget'}),label=u'')

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return MaybeLessSpamComment

    def get_comment_create_data(self):
        # Use the data of the superclass 
        data = super(MaybeLessSpamCommentForm, self).get_comment_create_data()
        return data




