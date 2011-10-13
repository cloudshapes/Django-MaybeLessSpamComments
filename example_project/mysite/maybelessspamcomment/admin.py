from maybelessspamcomment.models import MaybeLessSpamComment
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.encoding import force_unicode
from django.utils.text import capfirst
from django.core.exceptions import PermissionDenied
from django.contrib.admin.util import model_ngettext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django import forms, template
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response


class MaybeLessSpamCommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_akismet_spam', 'is_public', 'is_removed')}
        ),
     )

    list_display = ('name', 'content_type', 'content_object',  'object_pk', 'comment',  'ip_address', 'submit_date', 'is_akismet_spam', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed', 'is_akismet_spam', 'content_type')
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)
    raw_id_fields = ('user', )
    search_fields = ('comment', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')

    # Extend this models get_urls so that we can include our 'delete_akismet_spam' view. 
    def get_urls(self):
        urls = super(MaybeLessSpamCommentAdmin, self).get_urls()
        my_urls = patterns('',
             (r'^delete_akismet_spam/$', self.admin_site.admin_view(self.delete_akismet_spam))
        )
        return my_urls + urls

    # Extend this so can add in the has_delete_permission property to the changelist_view.
    def changelist_view(self, request, extra_context=None):
	extra_context={ 'has_delete_permission': self.has_delete_permission(request) }
        return super(MaybeLessSpamCommentAdmin, self).changelist_view(request, extra_context)


    # From http://docs.djangoproject.com/en/dev/ref/contrib/admin/#adding-views-to-admin-sites:
    # Any view you render that uses the admin templates, or extends the base admin template, should provide the current_app argument to RequestContext or Context 
    # when rendering the template. It should be set to either self.name if your view is on an AdminSite or self.admin_site.name if your view is on a ModelAdmin.

    # View below is 'inspired' - based on - delete_view function in contrib/admin/options.py, and delete_selected function in contrib/admin/actions.py
    def delete_akismet_spam(self, request):
        opts = self.model._meta
        app_label = opts.app_label
	perms_needed = False

	# Check that the user has delete permission for the actual model
	if not self.has_delete_permission(request):
		perms_needed = True
	if not self.has_delete_permission(request):
        	raise PermissionDenied


	spam_comments_queryset = MaybeLessSpamComment.objects.all().filter(is_akismet_spam='True')
	n_spam_comments = spam_comments_queryset.count()

	# The user has already confirmed the deletion.
	# Do the deletion and return a None to display the change list view again.
        if request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            if n_spam_comments:
                for obj in spam_comments_queryset:
                    obj_display = force_unicode(obj)
                    self.log_deletion(request, obj, obj_display)
		    obj.delete()
                # queryset.delete()
                self.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                    "count": n_spam_comments, "items": model_ngettext(opts, n_spam_comments)
                })
            return HttpResponseRedirect("../")

	title_string = "Delete  %s Akismet-marked spam comments - are you sure?" % n_spam_comments
	deletable_objects = []
	for obj in spam_comments_queryset:
	        deletable_objects.append([mark_safe(u'%s: <a href="../%s/">%s</a>' % (escape(force_unicode(capfirst(opts.verbose_name))), obj.pk, escape(obj))), []])

        # 'current_app':self.admin_site.name
        context = {
            "title": _(title_string),
	    "n_spam_comment": n_spam_comments,
            "perms_lacking": perms_needed,
            "opts": opts,
            "root_path": self.admin_site.root_path,
	    "deletable_objects": deletable_objects,
            "app_label": app_label,
        }
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response('admin/%s/delete_akismet_spam.html' % app_label, context, context_instance=context_instance )

admin.site.register(MaybeLessSpamComment, MaybeLessSpamCommentAdmin)




