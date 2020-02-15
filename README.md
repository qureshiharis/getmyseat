# getmyseat
Web engineering project (info center)

REQUIREMENTS:

1. Flask framework for Web development using Python
2. SQLAlchemy for database connectivity and queries in Python
3. psycopg2 is a PostgreSQL Database Adapter
4. Gunicorn is used to speed up the accessibility. It supports multiple users to access the website, quickly loads the page.

Deployed using Heroku 
Procfile is used to tell Heroku two things;
1. What is the type of file ("web")
2. Which file to run first ("application", application.py the main file)
