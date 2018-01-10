drScratch
=========

drScratch is an analytical tool that evaluates your Scratch projects in a variety of computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelization, flow control, user interactivity and data representation. This analyzer is a helpful tool to evaluate your own projects, or those of your Scratch students.

You can try a beta version of drScratch at http://drscratch.org

------------------------------------

+Dependencies
 +
 +* Python 2.7.14
 +* Django 1.7 python frameWork
 +* kurt python module
 +* hairball python module
 +* gspread python module
 +* oauth2client python module
 
+====================================================
+============= kurt
https://pypi.python.org/pypi/kurt
Library for reading/writing MIT's Scratch file format.
Kurt is a Python library for working with Scratch project files.
## Installation
pip install kurt

+====================================================
+============= hairball
https://pypi.python.org/pypi/hairball/0.3
https://github.com/ucsb-cs-education/hairball
Hairball is a plugin-able framework useful for static analysis of Scratch projects.
## Installation
pip install hairball
Once you installed the original hairball distribution you should replace its files with the ones in our fork: https://github.com/jemole/hairball

+====================================================
+============== Django
URL : https://docs.djangoproject.com/en/1.7/
URL TUTORIAL : https://docs.djangoproject.com/en/1.7/intro/tutorial01/
$ python manage.py makemigrations app
$ python manage.py sqlmigrate app 0001
$ python manage.py migrate
$ python manage.py runserver

+====================================================
+============== gspread oauth2client ( Python Lib )
URL : https://github.com/burnash/gspread
URL TUTORIAL : https://github.com/burnash/gspread
## Installation
$ pip install gspread oauth2client 

+====================================================
+============== Google Drive and Google Sheets API
URL : https://console.developers.google.com
-Login
-habilitar Google Drive API
-habilitar Google Sheets API
-Credenciales / CREAR miembro (cuentas de servicios)