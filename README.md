# getmyseat
Web engineering project (info center)

REQUIREMENTS:

Flask framework for Web development using Python
SQLAlchemy for database connectivity and queries in Python
psycopg2 is a PostgreSQL Database Adapter
Gunicorn is used to speed up the accessibility. It supports multiple users to access the website, quickly loads the page.

Deployed using Heroku 
Procfile is used to tell Heroku two things;
1. What is the type of file ("web")
2. Which file to run first ("application", application.py the main file)
