

Example Project Incorporating django-maybelessspamcomments:
----------------------------------------------------------------

1. Requires:
- sqlite3 installed.
- 'markdown': On Ubuntu: "aptitude install python-markdown"

2. Setup:

a. Settings.py:
- Database path currently set to:
 'NAME': './mysite.db',  # Or path to database file if using sqlite3.

Clearly you need to change this to a path to your sqlite3 database. If you haven't created one (but have installed sqlite3) don't panic, when you first run "python manage.py syncdb" this will create a sample database.

- You need to ammend the AKISMET_API_KEY, RECAPTCHA_PUBLIC_KEY and the RECAPTCHA_PRIVATE_KEY settings to your own keys. These should work on  http://127.0.0.1:8000/. However for the "RECAPTCHA" to work when run from a proper webserver (e.g. Apache) you will need to be setup with the domain you registered with RECAPTCHA. 

b. Syncdb.
You should now be away to go ...

3. Running the sample project:
- Sample model with comment at http://127.0.0.1:8000/model2/1/
- Admin at http://127.0.0.1:8000/admin, username/password currently set to r/r.












