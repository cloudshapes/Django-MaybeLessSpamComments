

Django MaybeLessSpamComments
=============================

**Less spam in Django comments using Akismet, Recaptcha and profanity checking**

MaybeLessSpamComments is a set of apps that look to restrict the quantity of spam in Django comments. It's called "maybe" as spammers are ingenious at finding ways around anti-spam protection. The code is compatible with:

* Django 1.3.1.
* Grapelli (https://github.com/sehmaschine/django-grappelli, version on 13/10/11), and Filebrowser (https://github.com/sehmaschine/django-filebrowser, version on 13/10/11)

The code includes:

* A small extension to the standard Django Admin interface: i.e. a link that enables the quick deletion of all comments that have been flagged as spam by Akismet.
* A fully working sample Django project.


Derived From:
----------------

The code in this set of applications is influenced by, and uses open-source code from:

* `James Bennett's <http://www.b-list.org/>`_ `"Practical Django Projects" book <http://goo.gl/mk9c5>`_ - particularly the end of Chapter 7 "Finishing the Weblog"
* The following Python Akismet library: http://www.voidspace.org.uk/python/modules.shtml#akismet 
* The official Recaptcha Client download: http://pypi.python.org/pypi/recaptcha-client#downloads
* Code from http://code.google.com/p/recaptcha-django/

Please note that the Akismet library and the two Recaptcha libraries are both included in this repository.


Requirements
------------

MaybeLessSpamComments 0.6 requires:

* Django 1.3 (http://www.djangoproject.com)
* The Python "markdown" library. To install "markdown" on Ubuntu: "aptitude install python-markdown"


Installation and Setup:
------------------------
1. Get an Akismet API key: https://akismet.com/signup/. This can be free, it's up to you. Retrieve a personal key.
2. Obtain a public and private ReCaptcha key: https://www.google.com/recaptcha/admin/create
3. Download the MaybeLessSpamComments from GitHub. Place the four apps (i.e. 'akismet', 'maybelessspamcomment', 'recaptcha' and 'recaptcha_django') that can be found in the "maybelesscomments" folder on your PYTHON_PATH. 
4. Ammend your projects urls.py file as follows::

	(r'^comments/', include('maybelessspamcomment.urls')),

5. In settings.py: add the following to INSTALLED_APPS::

	'maybelessspamcomment',
	'django.contrib.comments',
	'django.contrib.markup',
	'recaptcha',
	'recaptcha_django',

 
6. **N.B.**: 'maybelessspamcomment' in INSTALLED_APPS *must* appear above 'django.contrib.comments' (to do with retrieving comment templates).


7. In settings.py: add the following to MIDDLEWARE_CLASSES: (N.B.: add at the **end** of MIDDLEWARE_CLASSES)::

	'recaptcha_django.middleware.ReCaptchaMiddleware',

8. In settings.py, add the following settings::

	AKISMET_API_KEY='your-akismet-key'
	COMMENTS_APP = 'maybelessspamcomment'
	MAX_COMMENT_LENGTH=500 # Maximum length of any comment
	COMMENT_EMAIL_NOTIFICATION_FLAG=False # Whether to be notified via email of comments being successfully posted.
	COMMENT_MODERATE_AFTER=15 # No. of days after which all comments must be moderated.
	COMMENT_CLOSE_AFTER=30 # No. of days after which comments are no longer allowed.
	# ReCaptcha Key's:
	RECAPTCHA_PUBLIC_KEY='your-recaptcha-public-key'
	RECAPTCHA_PRIVATE_KEY='your-recaptcha-private-key'
	BAD_WORDS_FILE='comments/bad-words.txt'

9. If you wish email notification of comments being posted, you need to add the following in settings.py::

	# Email settings
	EMAIL_HOST = '<host>'
	EMAIL_HOST_USER ='<username>'
	EMAIL_HOST_PASSWORD ='<password>'
	EMAIL_PORT = <port>
	EMAIL_USE_TLS = True
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


10. In settings.py, add the following::

	from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
	TEMPLATE_CONTEXT_PROCESSORS += (
	     'django.core.context_processors.request',
	) 

11. In the model.py of the model to which you wish to attach comments:

* Add "enable_comments = models.BooleanField(default=True)" to your model
* Ensure that the model also has a "pub_date" DateTimeField field, e.g. "pub_date = models.DateTimeField(default=datetime.datetime.now)"
* Add the following to the bottom of your models.py file::

	# Register MaybeLessSpamCommentModerator moderator for <your_model>
	from django.contrib.comments.moderation import moderator
	from maybelessspamcomment.moderation import MaybeLessSpamCommentModerator
	moderator.register(<your_model>, MaybeLessSpamCommentModerator)

12. Now sync your database ("python manage.py syncdb")

13. To enable comments in your models templates, simply add the following to the template .html file::

	{% load comments %}
	{% render_comment_form for [your_model] %}
	{% render_comment_list for [your_model] %}


14. The project provides its own basic styling for the comments. The styling is delivered as inline CSS via the  "maybelessspamcomment/templates/comments/comments_style.html" template. If you wish to style the comments yourself either:

* Create your own "maybelessspamcomment/templates/comments/comments_style.html" template in your own projects template folder. 
* Or, perhaps, more elegantly, provide an empty "maybelessspamcomment/templates/comments/comments_style.html" template in your own projects template folder and style the comments using your projects main CSS files.


Example Project:
------------------
The "example_project" folder contains a sample project that uses Sqlite3, so if you have that installed, simply run "python manage.py runserver" from within the "example_project/mysite" folder. Without the Akismet or Recaptcha keys those particular items of functionality won't work, but there's not much more you need to do at this stage.


Documentation
-------------
Further detail documentation coming soon, will be up on http://www.cloudshapes.co.uk/ (at some point).



