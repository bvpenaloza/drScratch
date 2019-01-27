#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.template import Context, loader
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate,get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext as _
from django.utils.encoding import force_bytes
from django.db.models import Avg
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.views import generic
from app.models import Project, Dashboard, Attribute
from app.models import Dead, Sprite, Mastery, Duplicate, File, CSVs
from app.models import Teacher, Student, Classroom, Stats
from app.models import Organization, OrganizationHash
from app.forms import UploadFileForm, UserForm, NewUserForm, UrlForm, TeacherForm
from app.forms import OrganizationForm, OrganizationHashForm, LoginOrganizationForm
from django.contrib.auth.models import User
from datetime import datetime,timedelta,date
from django.contrib.auth.decorators import login_required
from email.MIMEText import MIMEText
from django.utils.encoding import smart_str
import smtplib
import email.utils
import os
import ast
import json
import sys
import urllib2
import shutil
import unicodedata
import csv
import kurt
import zipfile
from zipfile import ZipFile
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Global variables
pMastery = "hairball -p mastery.Mastery "
pDuplicateScript = "hairball -p duplicate.DuplicateScripts "
pSpriteNaming = "hairball -p convention.SpriteNaming "
pDeadCode = "hairball -p blocks.DeadCode "
pInitialization = "hairball -p initialization.AttributeInitialization "
diccionarioglobal = []

#_____________________________ MAIN ______________________________________#

def main(request):
    """Main page"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    # The first time one user enters
    # Create the dashboards associated to users
    createDashboards()
    return render_to_response('main/main.html',
                                {'user':user},
                                RC(request))

#___________________________ REDIRECT ____________________________________#

def redirectMain(request):
    """Page not found redirect to main"""
    return HttpResponseRedirect('/')

#_______________________________ ERROR ___________________________________#

def error404(request):
    response = render_to_response('404.html', {},
                                  context_instance = RC(request))
    response.status_code = 404
    return response

def error500(request):
    response = render_to_response('500.html', {},
                                  context_instance = RC(request))
    return response

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#-------------------------------------------------------------------------


#_______________________ dashpy criterios perceptivos ___________________#

def dashpy(request): 
    global diccionarioglobal
    diccionary = diccionarioglobal
    print (diccionarioglobal)
    print (diccionary)
    print ("fuera del for")
    for obj in diccionary:
        print(obj.dataRepresentation)
        print(obj.mecanica)
        print(obj)
        print("dentro del for")
    return render_to_response("dashpy/perceptivos.html", {'dic':diccionary} , context_instance = RC(request))


#_______________________ TO UNREGISTERED USER ___________________________#

def selector(request):
    global diccionarioglobal
    if request.method == 'POST':
        error = False
        id_error = False
        no_exists = False
        if "_upload" in request.POST:
            d = uploadUnregistered(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            else:

                dic = {'url': ""}
                d.update(dic)
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
        elif '_url' in request.POST:
            d = urlUnregistered(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            elif d['Error'] == 'id_error':
                id_error = True
                return render_to_response('main/main.html',
                            {'id_error':id_error},
                            RC(request))
            elif d['Error'] == 'no_exists':
                no_exists = True
                return render_to_response('main/main.html',
                    {'no_exists':no_exists},
                    RC(request))
            else:
                form = UrlForm(request.POST)
                url = request.POST['urlProject']
                dic = {'url': url}
                d.update(dic)
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
        elif '_path' in request.POST:
            if (request.POST['mailPath'] != '' and len(request.FILES.getlist('zipPath'))>0): 
                mail = str(request.POST['mailPath'])
                scope = ['https://www.googleapis.com/auth/drive']
                GoogleAuth = ServiceAccountCredentials.from_json_keyfile_name('client_secret2.json', scope)
                client = gspread.authorize(GoogleAuth)
                x = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                nameFile = 'PRG '+ x 
                sh = client.create(nameFile)
                sh.share('valeria.leon@progracademy.org', perm_type='user', role='writer')
                #sh.share('bvpenaloza.11@gmail.com', perm_type='user', role='writer')
                sh.share(mail, perm_type='user', role='writer')
                sheet = client.open(nameFile).sheet1
                listValues = ['id', 'filename', 'method', 'time', 'language', 'level',  'score', 'abstraction', 'parallelization', 'logic', 'synchronization', 'flowControl', 'userInteractivity', 'dataRepresentation' , 'spriteNaming' , 'initialization', 'deadCode', 'duplicateScript', 'puntaje','dialogos','eventos','puntuacion','acciones','objetivo','mecanica' ]
                updateSheet(listValues, 1, sheet)
                d = ''
                row = 2  
                diccionary = []
                for file in request.FILES.getlist('zipPath'):
                    d = uploadUnregisteredSecond(request,file)
                    f = File.objects.latest('id')
                    diccionary.append(f)
                    level='basic'
                    if (int(f.score) >= 15):
                        level='master'
                    elif (int(f.score) > 7):
                        level='developing'
                    listValues = [f.id, f.filename, f.method, f.time, f.language, level, f.score, f.abstraction, f.parallelization, f.logic, f.synchronization, f.flowControl, f.userInteractivity, f.dataRepresentation , f.spriteNaming , f.initialization, f.deadCode, f.duplicateScript, f.puntaje, f.dialogos, f.eventos, f.puntuacion, f.acciones, f.objetivo, f.mecanica]
                    updateSheet(listValues, row, sheet)
                    row += 1
                diccionarioglobal = diccionary    
                return render_to_response("upload/dashboard-unregistered-folder.html", {'diccionary': diccionary} )
            diccionarioglobal = diccionary       
            return HttpResponseRedirect('/') 
    else:
        return HttpResponseRedirect('/')


def updateSheet(listValues, row, sheet):
    colum = 1
    for token in listValues:
        sheet.update_cell(row, colum, token)
        colum += 1

def handler_upload(fileSaved, counter):
    """ Necessary to uploadUnregistered"""
    # If file exists,it will save it with new name: name(x)
    if os.path.exists(fileSaved):
        counter = counter + 1
        #Check the version of Scratch 1.4Vs2.0
        version = checkVersion(fileSaved)
        if version == "2.0":
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb2"
            else:
                fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb2"
        else:
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb"
            else:
                fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb"


        file_name = handler_upload(fileSaved, counter)
        return file_name
    else:
        file_name = fileSaved
        return file_name

def checkVersion(fileName):
    extension = fileName.split('.')[-1]
    if extension == 'sb2':
        version = '2.0'
    else:
        version = '1.4'
    return version


#_______________________Project Analysis Project___________________#

def uploadUnregistered(request):
    """Upload file from form POST for unregistered users"""
    if request.method == 'POST':
        #Revise the form in main
        #If user doesn't complete all the fields,it'll show a warning
        try:
            file = request.FILES['zipFile']
        except:
            d = {'Error': 'MultiValueDict'}
            return  d
        # Create DB of files
        now = datetime.now()
        method = "project"
        fileName = File (filename = file.name.encode('utf-8'),
                        organization = "",
                        method = method , time = now,
                        score = 0, abstraction = 0, parallelization = 0,
                        logic = 0, synchronization = 0, flowControl = 0,
                        userInteractivity = 0, dataRepresentation = 0,
                        spriteNaming = 0 ,initialization = 0,
                        deadCode = 0, duplicateScript = 0, eventos = 0,
                        puntuacion = 0, puntaje = 0, mecanica = 0,
                        dialogos = 0, acciones = 0, objetivo = 0)
        fileName.save()
        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Version of Scratch 1.4Vs2.0
        version = checkVersion(fileName.filename)
        if version == "1.4":
            fileSaved = dir_zips + str(fileName.id) + ".sb"
        else:
            fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Create log
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
        str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
        "Time: " + str(fileName.time) + "\n")

        # Save file in server
        counter = 0
        file_name = handler_upload(fileSaved, counter)


        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        #Create 2.0Scratch's File
        file_name = changeVersion(request, file_name)

        # Analyze the scratch project
        try:
            d = analyzeProject(request, file_name, fileName)

        except:
            #There ir an error with kutz or hairball
            #We save the project in folder called error_analyzing
            fileName.method = 'project/error'
            fileName.save()
            oldPathProject = fileSaved
            newPathProject = fileSaved.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             fileSaved.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}
            return d
        # Show the dashboard
        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'
        return d
    else:
        return HttpResponseRedirect('/')



def changeVersion(request, file_name):
    p = kurt.Project.load(file_name)
    p.convert("scratch20")
    p.save()
    file_name = file_name.split('.')[0] + '.sb2'
    return file_name



def uploadUnregisteredSecond(request,file):
    """Upload file from form POST for unregistered users"""
    if request.method == 'POST':
        #Revise the form in main
        # Create DB of files
        now = datetime.now()
        method = "project"
        fileName = File (filename = file.name.encode('utf-8'),
                        organization = "",
                        method = method , time = now,
                        score = 0, abstraction = 0, parallelization = 0,
                        logic = 0, synchronization = 0, flowControl = 0,
                        userInteractivity = 0, dataRepresentation = 0,
                        spriteNaming = 0 ,initialization = 0,
                        deadCode = 0, duplicateScript = 0, eventos = 0,
                        puntuacion = 0, puntaje = 0, mecanica = 0,
                        dialogos = 0, acciones = 0, objetivo = 0)
        fileName.save()
        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Version of Scratch 1.4Vs2.0
        version = checkVersion(fileName.filename)
        if version == "1.4":
            fileSaved = dir_zips + str(fileName.id) + ".sb"
        else:
            fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Create log
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
        str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
        "Time: " + str(fileName.time) + "\n")

        # Save file in server
        counter = 0
        file_name = handler_upload(fileSaved, counter)

        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        #Create 2.0Scratch's File
        file_name = changeVersion(request, file_name)

        # Analyze the scratch project
        d = analyzeProject(request, file_name, fileName)
    return d



#_______________________URL Analysis Project_________________________________#


def urlUnregistered(request):
    """Process Request of form URL"""
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            d = {}
            url = form.cleaned_data['urlProject']
            idProject = processStringUrl(url)
            if idProject == "error":
                d = {'Error': 'id_error'}
                return d
            else:
                try:
                    organization = ""
                    method = "url"
                    (pathProject, file) = sendRequestgetSB2(idProject, organization, method)
                except:
                    #When your project doesn't exist
                    d = {'Error': 'no_exists'}
                    return d
                try:
                    d = analyzeProject(request, pathProject, file)
                except:
                    #There ir an error with kutz or hairball
                    #We save the project in folder called error_analyzing
                    file.method = 'url/error'
                    file.save()
                    oldPathProject = pathProject
                    newPathProject = pathProject.split("/uploads/")[0] + \
                                     "/error_analyzing/" + \
                                     pathProject.split("/uploads/")[1]
                    shutil.copy(oldPathProject, newPathProject)
                    d = {'Error': 'analyzing'}
                    return d

                #Create Json
                djson = createJson(d)

                # Redirect to dashboard for unregistered user
                d['Error'] = 'None'
                return d
        else:
            d = {'Error': 'MultiValueDict'}
            return  d
    else:
        return HttpResponseRedirect('/')


def processStringUrl(url):
    """Process String of URL from Form"""
    idProject = ''
    auxString = url.split("/")[-1]
    if auxString == '':
        # we need to get the other argument
        possibleId = url.split("/")[-2]
        if possibleId == "#editor":
            idProject = url.split("/")[-3]
        else:
            idProject = possibleId
    else:
        if auxString == "#editor":
            idProject = url.split("/")[-2]
        else:
            # To get the id project
            idProject = auxString
    try:
        checkInt = int(idProject)
    except ValueError:
        idProject = "error"
    return idProject

def sendRequestgetSB2(idProject, organization, method):
    """First request to getSB2"""
    getRequestSb2 = "http://drscratch.cloudapp.net:8080/" + idProject
    fileURL = idProject + ".sb2"
    # Create DB of files
    now = datetime.now()
    fileName = File (filename = fileURL,
                     organization = organization,
                     method = method , time = now,
                     score = 0, abstraction = 0, parallelization = 0,
                     logic = 0, synchronization = 0, flowControl = 0,
                     userInteractivity = 0, dataRepresentation = 0,
                     spriteNaming = 0 ,initialization = 0,
                     deadCode = 0, duplicateScript = 0, eventos = 0,
                     puntuacion = 0, puntaje = 0, mecanica = 0,
                     dialogos = 0, acciones = 0, objetivo = 0)
    fileName.save()
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    fileSaved = dir_zips + str(fileName.id) + ".sb2"
    pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    logFile = open (pathLog + "logFile.txt", "a")
    logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
    str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
    "Time: " + str(fileName.time) + "\n")
    # Save file in server
    counter = 0
    file_name = handler_upload(fileSaved, counter)
    outputFile = open(file_name, 'wb')
    sb2File = urllib2.urlopen(getRequestSb2)
    outputFile.write(sb2File.read())
    outputFile.close()
    return (file_name, fileName)



#________________________ CREATE JSON _________________________________#

def createJson(d):
    flagsPlugin = {"Mastery":0, "DeadCode":0, "SpriteNaming":1, "Initialization":0, "DuplicateScripts":0}


#________________________ LEARN MORE __________________________________#

def learn(request,page):
    #Unicode to string(page)
    page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')

    dic = {'Pensamiento':'Logic',
           'Paralelismo':'Parallelism',
          'Representacion':'Data representation',
          'Sincronizacion':'Synchronization',
          'Interactividad':'User interactivity',
          'Control':'Flow control',
          'Abstraccion':'Abstraction'}

    if page in dic:
        page = dic[page]

    page = "learn/" + page + ".html"

    if request.user.is_authenticated():

        return render_to_response(page,
                                RC(request))
    else:

        return render_to_response(page,
                                RC(request))

def learnUnregistered(request):

    return render_to_response("learn/learn-unregistered.html",)

#________________________ COLLABORATORS _____________________________#

def collaborators(request):

    return render_to_response("main/collaborators.html",)


#________________________ TO REGISTER ORGANIZATION __________________#

def organizationHash(request):
    """Method for to sign up in the platform"""
    if request.method == "POST":
        form = OrganizationHashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/organizationHash')
    elif request.method == 'GET':
        return render_to_response("sign/organizationHash.html", context_instance = RC(request))

def signUpOrganization(request):
    """Method which allow to sign up organizations"""
    flagHash = 0
    flagName = 0
    flagEmail = 0
    flagForm = 0
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashkey = form.cleaned_data['hashkey']

            try:
                #This name already exists
                organization = Organization.objects.get(username=username)
                flagName = 1
                return render_to_response("sign/signup_error.html",
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm},
                                          context_instance = RC(request))
            except:
                try:
                    #This email already exists
                    email = Organization.objects.get(email=email)
                    flagEmail = 1
                    return render_to_response("sign/signup_error.html",
                                            {'flagName':flagName,
                                            'flagEmail':flagEmail,
                                            'flagHash':flagHash,
                                            'flagForm':flagForm},
                                            context_instance = RC(request))
                except:
                    try:
                        organizationHashkey = OrganizationHash.objects.get(hashkey=hashkey)
                        organizationHashkey.delete()
                        organization = Organization.objects.create_user(username = username, email=email, password=password, hashkey=hashkey)
                        organization = authenticate(username=username, password=password)
                        user=Organization.objects.get(email=email)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token=default_token_generator.make_token(user)
                        c = {
                                'email':email,
                                'uid':uid,
                                'token':token}

                        body = render_to_string("sign/email.html",c)
                        subject = "Welcome to Dr.Scratch for organizations"
                        sender ="no-reply@drscratch.org"
                        to = [email]
                        email = EmailMessage(subject,body,sender,to)
                        #email.attach_file("static/app/images/logo_main.png")
                        email.send()
                        login(request, organization)
                        return HttpResponseRedirect('/organization/' + organization.username)

                    except:
                        #Doesn't exist this hash
                        flagHash = 1

                        return render_to_response("sign/signup_error.html",
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm},
                                          context_instance = RC(request))
        else:
            flagForm = 1
            return render_to_response("sign/signup_error.html",
                  {'flagName':flagName,
                   'flagEmail':flagEmail,
                   'flagHash':flagHash,
                   'flagForm':flagForm},
                  context_instance = RC(request))

    elif request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/organization/' + request.user.username)
        else:
            return render_to_response("sign/organization.html", context_instance = RC(request))

#_________________________ TO SHOW ORGANIZATION'S DASHBOARD ___________#

def loginOrganization(request):
    """Log in app to user"""
    if request.method == 'POST':
        flag = False
        form = LoginOrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            organization = authenticate(username=username, password=password)
            if organization is not None:
                if organization.is_active:
                    login(request, organization)
                    return HttpResponseRedirect('/organization/' + organization.username)

            else:
                flag = True
                return render_to_response("password/user_doesntexist.html",
                                            {'flag': flag},
                                            context_instance=RC(request))

    else:
        return HttpResponseRedirect("/")


def logoutOrganization(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

def organization(request, name):
    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.user.username
            if username == name:
                user = Organization.objects.get(username=username)
                date_joined= user.date_joined
                end = datetime.today()
                y = end.year
                m = end.month
                d = end.day
                end = date(y,m,d)
                y = date_joined.year
                m = date_joined.month
                d = date_joined.day
                start = date(y,m,d)
                dateList = date_range(start, end)
                daily_score = []
                mydates = []

                for n in dateList:
                    mydates.append(n.strftime("%d/%m"))
                    points = File.objects.filter(organization=username).filter(time=n)
                    points = points.aggregate(Avg("score"))["score__avg"]
                    daily_score.append(points)

                for n in daily_score:
                    if n==None:
                        daily_score[daily_score.index(n)]=0


                dic={"date":mydates,"daily_score":daily_score,'username':username}

                return render_to_response("main/main_organization.html",
                        dic,
                        context_instance = RC(request))
            else:
                return render_to_response("sign/organization.html",
                                        context_instance = RC(request))
        return render_to_response("sign/organization.html", context_instance = RC(request))
    else:
        return HttpResponseRedirect("/")

#________________________ ANALYZE CSV FOR ORGANIZATIONS ____________#

def analyzeCSV(request):
    if request.method =='POST':
        if "_upload" in request.POST:
            csv_data = 0
            flag_csv = False
            file = request.FILES['csvFile']
            file_name = file.name.encode('utf-8')
            dir_csvs = os.path.dirname(os.path.dirname(__file__)) + "/csvs/" + file_name
            #Save file .csv
            with open(dir_csvs, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            infile = open(dir_csvs, 'r')
            dictionary = {}
            for line in infile:
                row = len(line.split(","))
                type_csv = ""
                organization = request.user.username
                if row == 2:
                    type_csv = "2_row"
                    code = line.split(",")[0]
                    url = line.split(",")[1]
                    url = url.split("\n")[0]
                    method = "csv"
                    print "ESTE" + str(url) + "VALE"
                    if url.isdigit():
                        print "FUNCIONA"
                        idProject = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            idProject = url.split("/")[-1]
                        elif slashNum == 5:
                            idProject = url.split('/')[-2]



                    try:
                        (pathProject, file) = sendRequestgetSB2(idProject, organization, method)
                        d = analyzeProject(request, pathProject, file)
                    except:
                        d = ["Error analyzing project", url]

                    dic = {}
                    dic[line] = d
                    dictionary.update(dic)
                elif row == 1:
                    type_csv = "1_row"
                    url = line.split("\n")[0]
                    method = "csv"
                    if url.isdigit():
                        idProject = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            idProject = url.split("/")[-1]
                        elif slashNum == 5:
                            idProject = url.split('/')[-2]



                    try:
                        (pathProject, file) = sendRequestgetSB2(idProject, organization, method)
                        d = analyzeProject(request, pathProject, file)
                    except:
                        d = ["Error analyzing project", url]

                    dic = {}
                    dic[url] = d
                    dictionary.update(dic)
            infile.close()
            try:
                csv_data = generatorCSV(request, dictionary, file_name, type_csv)
                flag_csv = True
            except:
                flag_csv = False


            if request.user.is_authenticated():
                username = request.user.username

            csv_save = CSVs(filename = file_name, directory = csv_data, organization = username)
            csv_save.save()

            return render_to_response("upload/dashboard-organization.html",
                                    {'username': username,
                                     'flag_csv': flag_csv,},
                                     context_instance=RC(request))

        elif "_download" in request.POST:
            """Export a CSV File"""
            if request.user.is_authenticated():
                username = request.user.username
            csv = CSVs.objects.latest('date')

            path_to_file = os.path.dirname(os.path.dirname(__file__)) + "/csvs/Dr.Scratch/" + csv.filename
            csv_data = open(path_to_file, 'r')
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(csv.filename)
            return response

    else:
        return HttpResponseRedirect("/organization")


#_________________________GENERATOR CSV FOR ORGANIZATION____________________________#

def generatorCSV(request, dictionary, file_name, type_csv):
    """Generator of a csv file"""
    csv_directory = os.path.dirname(os.path.dirname(__file__)) + "/csvs/Dr.Scratch/"
    csv_data = csv_directory + file_name
    writer = csv.writer(open(csv_data, "wb"))

    if request.LANGUAGE_CODE == "es":
        if type_csv == "2_row":
            writer.writerow(["CÓDIGO", "URL", "Mastery", "Abstracción", "Paralelismo", "Pensamiento lógico", "Sincronización", "Control de flujo", "Interactividad con el usuario", "Representación de la información", "Código repetido", "Nombres por defecto", "Código muerto",  "Inicialización atributos"])
        elif type_csv == "1_row":
            writer.writerow(["URL", "Mastery", "Abstracción", "Paralelismo", "Pensamiento lógico", "Sincronización", "Control de flujo", "Interactividad con el usuario", "Representación de la información", "Código repetido", "Nombres por defecto", "Código muerto",  "Inicialización atributos"])
        for key, value in dictionary.items():
            total = 0
            flag = False
            try:
                if value[0] == "Error analyzing project":
                    if type_csv == "2_row":
                        row1 = key.split(",")[0]
                        row2 = key.split(",")[1]
                        row2 = row2.split("\n")[0]
                        writer.writerow([row1, row2, "Error analizando el proyecto"])
                    elif type_csv == "1_row":
                        row1 = key.split(",")[0]
                        writer.writerow([row1, "Error analizando el proyecto"])
            except:
                total = 0
                row1 = key.split(",")[0]
                if type_csv == "2_row":
                    row2 = key.split(",")[1]
                    row2 = row2.split("\n")[0]

                for key, subvalue in value.items():
                    if key == "duplicateScript":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row11 = sub2value
                    if key == "spriteNaming":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row12 = sub2value
                    if key == "deadCode":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row13 = sub2value
                    if key == "initialization":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row14 = sub2value

                for key, value in value.items():
                    if key == "mastery":
                        for key, subvalue in value.items():
                            if key!="maxi" and key!="points":
                                if key == "Paralelismo":
                                    row5 = subvalue
                                elif key == "Abstracción":
                                    row4 = subvalue
                                elif key == "Pensamiento lógico":
                                    row6 = subvalue
                                elif key == "Sincronización":
                                    row7 = subvalue
                                elif key == "Control de flujo":
                                    row8 = subvalue
                                elif key == "Interactividad con el usuario":
                                    row9 = subvalue
                                elif key == "Representación de la información":
                                    row10 = subvalue
                                total = total + subvalue
                        row3 = total
                if type_csv == "2_row":
                    writer.writerow([row1,row2,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
                elif type_csv == "1_row":
                    writer.writerow([row1,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
    else:
        if type_csv == "2_row":
            writer.writerow(["CODE", "URL", "Mastery", "Abstraction", "Parallelism", "Logic", "Synchronization", "Flow control", "User interactivity", "Data representation", "Duplicate script", "Sprites naming", "Dead code",  "Sprite attributes"])
        elif type_csv == "1_row":
            writer.writerow(["URL", "Mastery", "Abstraction", "Parallelism", "Logic", "Synchronization", "Flow control", "User interactivity", "Data representation", "Duplicate script", "Sprites naming", "Dead code",  "Sprite attributes"])

        for key, value in dictionary.items():
            total = 0
            flag = False
            try:
                if value[0] == "Error analyzing project":
                    if type_csv == "2_row":
                        row1 = key.split(",")[0]
                        row2 = key.split(",")[1]
                        row2 = row2.split("\n")[0]
                        writer.writerow([row1, row2, "Error analyzing project"])
                    elif type_csv == "1_row":
                        row1 = key.split(",")[0]
                        writer.writerow([row1, "Error analyzing project"])
            except:
                total = 0
                row1 = key.split(",")[0]
                if type_csv == "2_row":
                    row2 = key.split(",")[1]
                    row2 = row2.split("\n")[0]

                for key, subvalue in value.items():
                    if key == "duplicateScript":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row11 = sub2value
                    if key == "deadCode":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row12 = sub2value
                    if key == "initialization":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row13 = sub2value
                    if key == "spriteNaming":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row14 = sub2value

                for key, value in value.items():
                    if key == "mastery":
                        for key, subvalue in value.items():
                            if key!="maxi" and key!="points":
                                if key == "Abstraction":
                                    row4 = subvalue
                                elif key == "Parallelism":
                                    row5 = subvalue
                                elif key == "Logic":
                                    row6 = subvalue
                                elif key == "Synchronization":
                                    row7 = subvalue
                                elif key == "Flow control":
                                    row8 = subvalue
                                elif key == "User interactivity":
                                    row9 = subvalue
                                elif key == "Data representation":
                                    row10 = subvalue
                                total = total + subvalue
                        row3 = total
                if type_csv == "2_row":
                    writer.writerow([row1,row2,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
                elif type_csv == "1_row":
                    writer.writerow([row1,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
    return csv_data



#________________________ TO REGISTER USER __________________________#

def createUserHash(request):
    """Method for to sign up in the platform"""
    logout(request)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            nickName = form.cleaned_data['nickname']
            emailUser = form.cleaned_data['emailUser']
            passUser = form.cleaned_data['passUser']
            user = User.objects.create_user(nickName, emailUser, passUser)
            return render_to_response("profile.html", {'user': user}, context_instance=RC(request))
    elif request.method == 'GET':
        return render_to_response("sign/createUserHash.html", context_instance = RC(request))

def signUpUser(request):
    form = TeacherForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            hashkey = form.cleaned_data['hashkey']
            #classroom = form.cleaned_data['classroom']
            invite(request, username, email, hashkey)
            teacher = Teacher(teacher = request.user, username = username,
                              password = password, email = email,
                              hashkey = hashkey)
            teacher.save()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

    elif request.method == 'GET':
        return render_to_response("sign/createUser.html", context_instance = RC(request))

def loginUser(request):
    """Log in app to user"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/myDashboard')
            else:
                flag = True
                return render_to_response("password/user_doesntexist.html",
                                            {'flag': flag},
                                            context_instance=RC(request))

    else:
        return HttpResponseRedirect("/")


def logoutUser(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

#_________________________ CHANGE PASSWORD __________________________________#

def changePwd(request):
    if request.method == 'POST':
        recipient = request.POST['email']
        try:
            user=Organization.objects.get(email=recipient)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)

            c = {
                    'email':recipient,
                    'uid':uid,
                    'token':token,
                    'id':user.username}

            body = render_to_string("password/email.html",c)

            try:
                subject = "Dr.Scratch: Did you forget your password?"
                sender ="no-reply@drscratch.org"
                to = [recipient]
                email = EmailMessage(subject,body,sender,to)
                #email.attach_file("static/app/images/logo_main.png")
                email.send()
                return render_to_response("password/email_sended.html",
                                        context_instance=RC(request))

            except:
                 return render_to_response("password/user_doesntexist.html",
                                           context_instance=RC(request))
        except:
            return render_to_response("password/user_doesntexist.html",
                                       context_instance=RC(request))
    else:
        return render_to_response("password/password.html",
                                   context_instance=RC(request))

def reset_password_confirm(request,uidb64=None,token=None,*arg,**kwargs):
    UserModel = get_user_model()
    try:
        uid=urlsafe_base64_decode(uidb64)
        user=Organization._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if request.method == "POST":
        flag_error = False
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST['password']
            new_confirm = request.POST['confirm']
            if new_password == "":
                return render_to_response("password/new_password.html",
                        context_instance=RC(request))

            elif new_password == new_confirm:
                user.set_password(new_password)
                user.save()
                return render_to_response("sign/organization.html",
                                            context_instance = RC(request))
            else:
                flag_error = True
                return render_to_response("password/new_password.html",
                                    {'flag_error':flag_error},
                                    context_instance=RC(request))

    else:
         if user is not None and default_token_generator.check_token(user, token):
             return render_to_response("password/new_password.html",
                                        context_instance=RC(request))
         else:
             return render_to_response("sign/organization.html",
                        context_instance = RC(request))

#_______________________ STATISTICS _________________________________#

def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]

def statistics(request):
    """ Initializing variables"""
    start = date(2015,8,1)
    end = datetime.today()
    y = end.year
    m = end.month
    d = end.day
    end = date(y,m,d)
    dateList = date_range(start, end)
    mydates=[]
    for n in dateList:
        mydates.append(n.strftime("%d/%m")) #used for x axis in

    """This final section stores all data for the template"""

    obj= Stats.objects.order_by("-id")[0]
    data = {"date":mydates,
             "dailyRate":obj.daily_score,
             "levels":{"basic":obj.basic,
                     "development":obj.development,
                     "master":obj.master},
             "totalProjects":obj.daily_projects,
             "skillRate":{"parallelism":obj.parallelism,
                          "abstraction":obj.abstraction,
                          "logic": obj.logic,
                          "synchronization":obj.synchronization,
                          "flowControl":obj.flowControl,
                          "userInteractivity":obj.userInteractivity,
                          "dataRepresentation":obj.dataRepresentation},
             "codeSmellRate":{"deadCode":obj.deadCode,
                              "duplicateScript":obj.duplicateScript,
                              "spriteNaming":obj.spriteNaming,
                              "initialization":obj.initialization }}
    return render_to_response("statistics/statistics.html",
                                    data, context_instance=RC(request))



#_______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(request,file_name, fileName):
    dictionary = {}
    if os.path.exists(file_name):
        list_file = file_name.split('(')
        if len(list_file) > 1:
            file_name = list_file[0] + '\(' + list_file[1]
            list_file = file_name.split(')')
            file_name = list_file[0] + '\)' + list_file[1]

        #Request to hairball
        #nota arreglar esta parte por que si no se instala los plugins por medio de setup hairball cambiar la direccion de los slash para windows
        #la direccion de /plugins/ son para servidores linux cambiar para que funcione
        metricPerceptivos = "hairball -d "+os.path.dirname(os.path.dirname(__file__))+ "/plugins/"+" -p perceptivos.Perceptivos " + file_name
        metricMastery = "hairball -p mastery.Mastery " + file_name
        metricDuplicateScript = "hairball -p \
                                duplicate.DuplicateScripts " + file_name
        metricSpriteNaming = "hairball -p convention.SpriteNaming " + file_name
        metricDeadCode = "hairball -p blocks.DeadCode " + file_name
        metricInitialization = "hairball -p \
                           initialization.AttributeInitialization " + file_name

        #Plug-ins not used yet
        #metricBroadcastReceive = "hairball -p
        #                          checks.BroadcastReceive " + file_name
        #metricBlockCounts = "hairball -p blocks.BlockCounts " + file_name
        #Response from hairball
        resultPerceptivos = os.popen(metricPerceptivos).read()
        resultMastery = os.popen(metricMastery).read()
        resultDuplicateScript = os.popen(metricDuplicateScript).read()
        resultSpriteNaming = os.popen(metricSpriteNaming).read()
        resultDeadCode = os.popen(metricDeadCode).read()
        resultInitialization = os.popen(metricInitialization).read()

        #Plug-ins not used yet
        #resultBlockCounts = os.popen(metricBlockCounts).read()
        #resultBroadcastReceive = os.popen(metricBroadcastReceive).read()
        #Create a dictionary with necessary information
        dictionary.update(procPerceptivos(request,resultPerceptivos, fileName))
        dictionary.update(procMastery(request,resultMastery, fileName))
        dictionary.update(procDuplicateScript(resultDuplicateScript, fileName))
        dictionary.update(procSpriteNaming(resultSpriteNaming, fileName))
        dictionary.update(procDeadCode(resultDeadCode, fileName))
        dictionary.update(procInitialization(resultInitialization, fileName))
        code = {'dupCode':DuplicateScriptToScratchBlock(resultDuplicateScript)}
        dictionary.update(code)
        code = {'dCode':DeadCodeToScratchBlock(resultDeadCode)}
        dictionary.update(code)
        #Plug-ins not used yet
        #dictionary.update(procBroadcastReceive(resultBroadcastReceive))
        #dictionary.update(procBlockCounts(resultBlockCounts))

        return dictionary
    else:
        return HttpResponseRedirect('/')

# __________________________ TRANSLATE MASTERY ______________________#

def translate(request,d, fileName):
    if request.LANGUAGE_CODE == "es":
        d_translate_es = {}
        d_translate_es['Abstracción'] = d['Abstraction']
        d_translate_es['Paralelismo'] = d['Parallelization']
        d_translate_es['Pensamiento lógico'] = d['Logic']
        d_translate_es['Sincronización'] = d['Synchronization']
        d_translate_es['Control de flujo'] = d['FlowControl']
        d_translate_es['Interactividad con el usuario'] = d['UserInteractivity']
        d_translate_es['Representación de la información'] = d['DataRepresentation']
        fileName.language = "es"
        fileName.save()
        return d_translate_es
    elif request.LANGUAGE_CODE == "en":
        d_translate_en = {}
        d_translate_en['Abstraction'] = d['Abstraction']
        d_translate_en['Parallelism'] = d['Parallelization']
        d_translate_en['Logic'] = d['Logic']
        d_translate_en['Synchronization'] = d['Synchronization']
        d_translate_en['Flow control'] = d['FlowControl']
        d_translate_en['User interactivity'] = d['UserInteractivity']
        d_translate_en['Data representation'] = d['DataRepresentation']
        fileName.language = "en"
        fileName.save()
        return d_translate_en
    else:
        return d


# __________________________ PROCESSORS _____________________________#

def procPerceptivos(request, lines, fileName):
    """Perceptivos """
    dic = {}
    lineas = lines.split('\n')
    print(lineas)
    print(lineas[0],"soy lineas 0")
    d = {}
    d = ast.literal_eval(lineas[1])
    #save in db
    fileName.puntaje = d["puntaje"]
    fileName.dialogos = d["Dialogos"]
    fileName.eventos = d["Eventos"]
    fileName.puntuacion = d["Puntuacion"]
    fileName.acciones = d["Acciones"]
    fileName.objetivo = d["Objetivo"]
    fileName.mecanica = d["Mecanica"]
    fileName.save()
    return dic

def procMastery(request,lines, fileName):
    """Mastery"""
    dic = {}
    lLines = lines.split('\n')
    d = {}
    d = ast.literal_eval(lLines[1])
    lLines = lLines[2].split(':')[1]
    points = int(lLines.split('/')[0])
    maxi = int(lLines.split('/')[1])

    #Save in DB
    fileName.score = points
    fileName.abstraction = d["Abstraction"]
    fileName.parallelization = d["Parallelization"]
    fileName.logic = d["Logic"]
    fileName.synchronization = d["Synchronization"]
    fileName.flowControl = d["FlowControl"]
    fileName.userInteractivity = d["UserInteractivity"]
    fileName.dataRepresentation = d["DataRepresentation"]
    fileName.save()

    #Translation
    d_translated = translate(request,d, fileName)

    dic["mastery"] = d_translated
    dic["mastery"]["points"] = points
    dic["mastery"]["maxi"] = maxi
    return dic

def procDuplicateScript(lines, fileName):
    """Return number of duplicate scripts"""
    dic = {}
    number = 0
    lLines = lines.split('\n')
    if len(lLines) > 2:
        number = lLines[1][0]
    dic["duplicateScript"] = dic
    dic["duplicateScript"]["number"] = number

    #Save in DB
    fileName.duplicateScript = number
    fileName.save()

    return dic


def procSpriteNaming(lines, fileName):
    """Return the number of default spring"""
    dic = {}
    lLines = lines.split('\n')
    number = lLines[1].split(' ')[0]
    lObjects = lLines[2:]
    lfinal = lObjects[:-1]
    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = str(number)
    dic['spriteNaming']['sprite'] = lfinal

    #Save in DB
    fileName.spriteNaming = str(number)
    fileName.save()

    return dic


def procDeadCode(lines, fileName):
    """Number of dead code with characters and blocks"""
    lLines = lines.split('\n')
    lLines = lLines[1:]
    lcharacter = []
    literator = []
    iterator = 0
    for frame in lLines:
        if '[kurt.Script' in frame:
            # Found an object
            name = frame.split("'")[1]
            lcharacter.append(name)
            if iterator != 0:
                literator.append(iterator)
                iterator = 0
        if 'kurt.Block' in frame:
            iterator += 1
    literator.append(iterator)

    number = len(lcharacter)
    dic = {}
    dic["deadCode"] = dic
    dic["deadCode"]["number"] = number
    for i in range(number):
        dic["deadCode"][lcharacter[i]] = literator[i]

    #Save in DB
    fileName.deadCode = number
    fileName.save()

    return dic


def procInitialization(lines, fileName):
    """Initialization"""
    dic = {}
    lLines = lines.split('.sb2')
    d = ast.literal_eval(lLines[1])
    keys = d.keys()
    values = d.values()
    items = d.items()
    number = 0

    for keys, values in items:
        list = []
        attribute = ""
        internalkeys = values.keys()
        internalvalues = values.values()
        internalitems = values.items()
        flag = False
        counterFlag = False
        i = 0
        for internalkeys, internalvalues in internalitems:
            if internalvalues == 1:
                counterFlag = True
                for value in list:
                    if internalvalues == value:
                        flag = True
                if not flag:
                    list.append(internalkeys)
                    if len(list) < 2:
                        attribute = str(internalkeys)
                    else:
                        attribute = attribute + ", " + str(internalkeys)
        if counterFlag:
            number = number + 1
        d[keys] = attribute
    dic["initialization"] = d
    dic["initialization"]["number"] = number

    #Save in DB
    fileName.initialization = number
    fileName.save()

    return dic

def DuplicateScriptToScratchBlock(code):
    try:
        code = code.split("\n")[2:][0]
        code = code[1:-1].split(",")
    except:
        code = ""

    return code

def DeadCodeToScratchBlock(code):
    try:
        code = code.split("\n")[2:-1]
        for n in code:
            n = n[15:-2]
    except:
        code = ""
    return code



#_________________________CSV File____________________________#
def exportCsvFile(request):
    """Export a CSV File"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="some.csv"'
    d = {"Abstraction": 2, "level": " Developing", "Parallelization": 1, "Logic": 1, "Synchronization": 2, "FlowControl": 2, "UserInteractivity": 1, "maxPoints": 21, "DataRepresentation": 1, "points": 10}
    writer = csv.writer(response)
    for key, value in d.items():
           writer.writerow([key, value])

    """
    writer = csv.writer(response)
    writer.writerow(['First row', 'Paco', '21', 'Madrid'])
    writer.writerow(['Second row', 'Lucia', '25', 'Quito'])
    """
    return response






##############################################################################
#                           UNDER DEVELOPMENT
##############################################################################

#________________________ DASHBOARD ____________________________#

def createDashboards():
    """Get users and create dashboards"""
    allUsers = User.objects.all()
    for user in allUsers:
        try:
            newdash = Dashboard.objects.get(user=user)
        except:
            fupdate = datetime.now()
            newDash = Dashboard(user=user.username, frelease=fupdate)
            newDash.save()

def myDashboard(request):
    """Dashboard page"""
    if request.user.is_authenticated():
        user = request.user.username
        # The main page of user
        # To obtain the dashboard associated to user
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        beginner = mydashboard.project_set.filter(level="beginner")
        developing = mydashboard.project_set.filter(level="developing")
        advanced = mydashboard.project_set.filter(level="advanced")
        return render_to_response("myDashboard/content-dashboard.html",
                                    {'user': user,
                                    'beginner': beginner,
                                    'developing': developing,
                                    'advanced': advanced,
                                    'projects': projects},
                                    context_instance=RC(request))
    else:
        user = None
        return HttpResponseRedirect("/")

def myProjects(request):
    """Show all projects of dashboard"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myProjects/content-projects.html",
                                {'projects': projects,
                                 'user':user},
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


def myRoles(request):
    """Show the roles in Doctor Scratch"""
    if request.user.is_authenticated():
        user = request.user.username
        return render_to_response("myRoles/content-roles.html",
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")



def myHistoric(request):
    """Show the progress in the application"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myHistoric/content-historic.html",
                                    {'projects': projects},
                                    context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


#________________________ PROFILE ____________________________#


def updateProfile(request):
    """Update the pass, email and avatar"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            newPass = form.cleaned_data['newPass']
            newEmail = form.cleaned_data['newEmail']
            choiceField = forms.ChoiceField(widget=forms.RadioSelect())
            return HttpResponseRedirect('/mydashboard')
        else:
            return HttpResponseRedirect('/')


def changePassword(request, new_password):
    """Change the password of user"""
    user = User.objects.get(username=current_user)
    user.set_password(new_password)
    user.save()

# ___________________ PROCESSORS OF PLUG-INS NOT USED YET ___________________#

#def procBlockCounts(lines):
#    """CountLines"""
#    dic = {}
#    dic["countLines"] = lines
#    return dic


#def procBroadcastReceive(lines):
#    """Return the number of lost messages"""
#    dic = {}
#    lLines = lines.split('\n')
    # messages never received or broadcast
#    laux = lLines[1]
#    laux = laux.split(':')[0]
#    dic["neverRB"] = dic
#    dic["neverRB"]["neverReceive"] = laux
#    laux = lLines[3]
#    laux = laux.split(':')[0]
#    dic["neverRB"]["neverBroadcast"] = laux

#    return dic


#_____________________ CREATE STATS OF ANALYSIS PERFORMED ___________#

def createStats(file_name, dictionary):
    flag = True
    return flag




#___________________________ UNDER DEVELOPMENT _________________________#

#UNDER DEVELOPMENT: Children!!!Carefull
def registration(request):
    """Registration a user in the app"""
    return render_to_response("formulary.html")


#UNDER DEVELOPMENT: Children!!!Carefull
def profileSettings(request):
    """Main page for registered user"""
    return render_to_response("profile.html")

#UNDER DEVELOPMENT:
#TO REGISTERED USER
def uploadRegistered(request):
    """Upload and save the zip"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = UploadFileForm(request.POST)
        # Analyze the scratch project and save in our server files
        fileName = handle_uploaded_file(request.FILES['zipFile'])
        # Analize project and to save in database the metrics
        d = analyzeProject(request,fileName)
        fupdate = datetime.now()
        # Get the short name
        shortName = fileName.split('/')[-1]
        # Get the dashboard of user
        myDashboard = Dashboard.objects.get(user=user)
        # Save the project
        newProject = Project(name=shortName, version=1, score=0, path=fileName, fupdate=fupdate, dashboard=myDashboard)
        newProject.save()
        # Save the metrics
        dmaster = d["mastery"]
        newMastery = Mastery(myproject=newProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], TotalPoints=dmaster["TotalPoints"])
        newMastery.save()
        newProject.score = dmaster["Total{% if forloop.counter0|divisibleby:1 %}<tr>{% endif %}Points"]
        if newProject.score > 15:
            newProject.level = "advanced"
        elif newProject.score > 7:
            newProject.level = "developing"
        else:
            newProject.level = "beginner"
        newProject.save()
        for charx, dmetrics in d["attribute"].items():
            if charx != 'stage':
                newAttribute = Attribute(myproject=newProject, character=charx, orientation=dmetrics["orientation"], position=dmetrics["position"], costume=dmetrics["costume"], visibility=dmetrics["visibility"], size=dmetrics["size"])
            newAttribute.save()

        iterator = 0
        for deadx in d["dead"]:
            if (iterator % 2) == 0:
                newDead = Dead(myproject=newProject, character=deadx, blocks=0)
            else:
                newDead.blocks = deadx
            newDead.save()
            iterator += 1

        newDuplicate = Duplicate(myproject=newProject, numduplicates=d["duplicate"][0])
        newDuplicate.save()
        for charx in d["sprite"]:
            newSprite = Sprite(myproject=newProject, character=charx)
            newSprite.save()
        return HttpResponseRedirect('/myprojects')

#_____ ID/BUILDERS ____________#

def idProject(request, idProject):
    """Resource uniquemastery of project"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    dmastery = {}
    project = Project.objects.get(id=idProject)
    item = Mastery.objects.get(myproject=project)
    dmastery = buildMastery(item)
    TotalPoints = dmastery["TotalPoints"]
    dsprite = Sprite.objects.filter(myproject=project)
    ddead = Dead.objects.filter(myproject=project)
    dattribute = Attribute.objects.filter(myproject=project)
    listAttribute = buildAttribute(dattribute)
    numduplicate = Duplicate.objects.filter(myproject=project)[0].numduplicates
    return render_to_response("project.html", {'project': project,
                                                'dmastery': dmastery,
                                                'lattribute': listAttribute,
                                                'numduplicate': numduplicate,
                                                'dsprite': dsprite,
                                                'Total points': TotalPoints,
                                                'ddead': ddead},
                                                context_instance=RequestContext(request))




def buildMastery(item):
    """Generate the dictionary with mastery"""
    dmastery = {}
    dmastery["Total points"] = item.TotalPoints
    dmastery["Abstraction"] = item.abstraction
    dmastery["Parallelization"] = item.paralel
    dmastery["Logic"] = item.logic
    dmastery["Synchronization"] = item.synchronization
    dmastery["Flow Control"] = item.flowcontrol
    return dmastery

def buildAttribute(qattribute):
    """Generate dictionary with attribute"""
    # Build the dictionary
    dic = {}
    for item in qattribute:
        dic[item.character] = {"orientation": item.orientation,
                                "position": item.position,
                                "costume": item.costume,
                                "visibility":item.visibility,
                                "size": item.size}
    listInfo = writeErrorAttribute(dic)
    return listInfo

#_______BUILDERS'S HELPERS ________#

def writeErrorAttribute(dic):
    """Write in a list the form correct of attribute plugin"""
    lErrors = []
    for key in dic.keys():
        text = ''
        dx = dic[key]
        if key != 'stage':
            if dx["orientation"] == 1:
                text = 'orientation,'
            if dx["position"] == 1:
                text += ' position, '
            if dx["visibility"] == 1:
                text += ' visibility,'
            if dx["costume"] == 1:
                text += 'costume,'
            if dx["size"] == 1:
                text += ' size'
            if text != '':
                text = key + ': ' + text + ' modified but not initialized correctly'
                lErrors.append(text)
            text = None
        else:
            if dx["background"] == 1:
                text = key + ' background modified but not initialized correctly'
                lErrors.append(text)
    return lErrors



# _________________________  _______________________________ #

def uncompress_zip(zip_file):
    unziped = ZipFile(zip_file, 'r')
    for file_path in unziped.namelist():
        if file_path == 'project.json':
            file_content = unziped.read(file_path)
    show_file(file_content)
