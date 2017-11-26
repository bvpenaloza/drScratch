drScratch
=========

drScratch is an analytical tool that evaluates your Scratch projects in a variety of computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelization, flow control, user interactivity and data representation. This analyzer is a helpful tool to evaluate your own projects, or those of your Scratch students.

You can try a beta version of drScratch at http://drscratch.org

------------------------------------

+Dependencies
 +============
 +
 +* Python 2.7.14
 +* Django 1.7
 +* kurt python module
 +* hairball python module




+============= kurt

https://pypi.python.org/pypi/kurt
Library for reading/writing MIT's Scratch file format.
Kurt is a Python library for working with Scratch project files.
## Installation
pip install kurt




+============= hairball

https://pypi.python.org/pypi/hairball/0.3
https://github.com/ucsb-cs-education/hairball
Hairball is a plugin-able framework useful for static analysis of Scratch projects.
## Installation
pip install hairball




+============== Django
URL : https://docs.djangoproject.com/en/1.7/
URL TUTORIAL : https://docs.djangoproject.com/en/1.7/intro/tutorial01/

$ python manage.py makemigrations app
        Migrations for 'polls':
        0001_initial.py:
            - Create model Question
            - Add field question to choice
            
$ python manage.py sqlmigrate app 0001
        BEGIN;
        CREATE TABLE "polls_question" ("id" serial NOT NULL PRIMARY KEY,);
        ALTER TABLE "polls_choice" ADD COLUMN "question_id" integer NOT NULL;
        COMMIT;

$ python manage.py migrate
        Operations to perform:
        Apply all migrations: admin, contenttypes, polls, auth, sessions
        Running migrations:
        Applying <migration name>... OK
