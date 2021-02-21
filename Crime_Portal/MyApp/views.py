from datetime import datetime
from django.http import request
import pandas as pd
from django.shortcuts import render, redirect
from MyApp.userdetails import User
from django.contrib import messages
from MyApp.models import Authentication, Registered_Users, WantedCriminals, AreaName, PSNames, GeneralDiary, GeneralDiaryByUsers, CrimeNews, LocalIntelligence
import random

obj = User()


def home(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    return render(request, 'index.html/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # User data retrieve from Database
        userdata = list(Authentication.objects.all().values_list())

        flag = False
        for element in userdata:                                        # Searching input data in database
            if element[1] == username and element[2] == password:
                flag = True
                break

        if flag:
            obj.set_name(username)
            return render(request, 'index.html/')
        else:
            messages.error(
                request, 'Invalid Email or Password ! ')
            return redirect('/login.html/')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        nid = request.POST['nid']
        image = request.FILES['image']

        if password == confirm_password:
            found = False
            data = Registered_Users.objects.all().values_list()
            for element in data:
                if(element[1] == email):
                    found = True
                    break

            if not found:
                # saving data to Registered Users
                dataX = Registered_Users(
                    email=email, firstname=firstname, lastname=lastname, password=password, nid=nid, image=image)
                dataX.save()

                # saving data to authentication
                auth_data = Authentication(
                    username=email, password=password, usertype="General User")
                auth_data.save()
                messages.error(
                    request, 'Account Creation Successfull !')
                return redirect('/signup.html/')
            else:
                messages.error(
                    request, 'This email is already registered ! Try contacting the administrator for recovery process ')
            return redirect('/signup.html/')
        else:
            messages.error(
                request, 'Passwords does not match ! ')
            return redirect('/signup.html/')
    else:
        return render(request, 'signup.html/')


def aboutus(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    return render(request, 'aboutus.html/')


def crimenews(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    data = CrimeNews.objects.all().order_by('-date')
    return render(request, 'crimenews.html/', {'data': data})


def localintelligence(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    if request.method == 'GET':
        data = PSNames.objects.all().order_by('psname')
        return render(request, 'localintelligence.html/', {'Data': data})
    if request.method == 'POST':
        email = obj.get_name()
        subject = request.POST['subject']
        psname = request.POST['psname']
        datetime = request.POST['datetime']
        files = request.FILES['file']
        details = request.POST['details']
        query = LocalIntelligence(email=email, subject=subject,
                                  psname=psname, date=datetime, files=files, details=details)
        query.save()

        messages.info(
            request, 'Your report submitted successfully! Thank you for your assistance. ')
        return redirect('/localintelligence.html')


def charts(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    data = []
    data2 = []
    refinedGeneralDiaryAreaQuery = []
    uniqueContents = []
    refinedGeneralDiaryGdTypeQuery = []
    uniqueContentGd = []

    GeneralDiaryAreaQuery = GeneralDiary.objects.all(
    ).values_list('area').order_by('area')

    GeneralDiaryGdTypeQuery = GeneralDiary.objects.all(
    ).values_list('gdtype').order_by('gdtype')

    for x in GeneralDiaryAreaQuery:
        refinedGeneralDiaryAreaQuery.append(x[0])

    for x in GeneralDiaryGdTypeQuery:
        refinedGeneralDiaryGdTypeQuery.append(x[0])
    # print(refinedGeneralDiaryAreaQuery)

    for item in refinedGeneralDiaryAreaQuery:
        if item not in uniqueContents:
            uniqueContents.append(item)

    for item in refinedGeneralDiaryGdTypeQuery:
        if item not in uniqueContentGd:
            uniqueContentGd.append(item)

    for i in uniqueContents:
        count = 0
        for j in refinedGeneralDiaryAreaQuery:
            if i == j:
                count = count+1
        data.append(count)

    for i in uniqueContentGd:
        count = 0
        for j in refinedGeneralDiaryGdTypeQuery:
            if i == j:
                count = count+1
        data2.append(count)
    # print(uniqueContentGd, data2)

    context = {'label': uniqueContents, 'data': data,
               'label2': uniqueContentGd, 'data2': data2}
    return render(request, 'charts.html/', context)


def wantedlist(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    if request.method == 'GET':
        data = WantedCriminals.objects.all().order_by('name')
        return render(request, 'wantedlist.html/', {'data': data})


def userDashboard(request):

    if(obj.get_name() == ""):
        return redirect('/login.html/')

    if request.method == 'POST':
        value = request.POST['gd_id']
        data = GeneralDiary.objects.all().filter(gd_id=value)
        context = {'data': data}
        return render(request, 'pdfgenerate.html/', context)

    value = obj.get_name()
    data = Registered_Users.objects.all().filter(email=value)
    # print(data)
    gddetails = GeneralDiary.objects.all().filter(email=value, verified=True)
    pendingGd = GeneralDiary.objects.all().filter(email=value, verified=False)
    # print(gddetails)
    context = {'data': data, 'gddetails': gddetails, 'nonVerified': pendingGd}
    return render(request, 'userDashboard.html/', context)


def pdfgenerate(request):
    return render(request, 'pdfgenerate.html/')


def gd(request):
    if(obj.get_name() == ""):
        return redirect('/login.html/')
    if request.method == 'GET':
        Dist_data = AreaName.objects.all().order_by('district')
        PS_data = PSNames.objects.all().order_by('psname')
        return render(request, 'gd.html/', {'Dist_data': Dist_data, 'PS_data': PS_data})
    if request.method == 'POST':
        value = obj.get_name()
        userDataList = Registered_Users.objects.all().filter(email=value).values_list()
        # print(userDataList)
        for element in userDataList:
            emails = element[1]
            name = element[2]+" "+element[3]
            nid = element[5]
        mobile = request.POST['mobile']
        issuedate = request.POST['issuedate']
        issuetime = request.POST['issuetime']
        gdtype = request.POST['gdtype']
        area = request.POST['area']
        psname = request.POST['psname']
        subject = request.POST['gdsubject']
        details = request.POST['gddetails']
        gd_id = random.randint(0, 3000)

        GD_Creation_queryset = GeneralDiary(email=emails, name=name, nid=nid,  mobile=mobile, issuedate=issuedate, issuetime=issuetime,
                                            gdtype=gdtype, area=area, psname=psname, subject=subject, details=details, gd_id=gd_id)
        GD_Record_command = GeneralDiaryByUsers(
            email=emails, gd_id=gd_id, creation_date=issuedate, creation_time=issuetime)

        GD_Creation_queryset.save()
        GD_Record_command.save()
        messages.info(
            request, 'Your General Diary submitted successfully! This is enlisted for review')
        return redirect('/gd.html/')


def Get_querter(hour):
    if hour >= 0 and hour <= 6:
        querter = 1
    if hour > 6 and hour <= 12:
        querter = 2
    if hour > 12 and hour <= 18:
        querter = 3
    if hour > 18 and hour <= 24:
        querter = 4
    return querter


def CountFrequency(my_list):

    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


def prediction(request):
    psFreq = []
    gdFreq = []
    crime_rate_perCountry = 0
    crime_rate_perArea = 0
    count = 0
    area = ""
    inputtime = ""
    qtr = 0

    if request.method == 'POST':
        #time = list(GeneralDiary.objects.all().values_list('issuetime'))
        count = GeneralDiary.objects.all().values('issuedate')
        area = request.POST['area']
        inputtime = request.POST['time']
        hour = int(inputtime[:2])
        qtr = Get_querter(hour)

        # print(querter)
        #print(area, inputtime,hour)
        data = GeneralDiary.objects.all().filter(area=area)
        # print(data)
        timelist = []
        gdtypelist = []
        psnamelist = []
        timelistX = []
        gdtypelistX = []
        psnamelistX = []

        for i in data:
            timelist.append(i.issuetime)
            gdtypelist.append(i.gdtype)
            psnamelist.append(i.psname)
        # all_data = timelist+gdtypelist+psnamelist
        # print(all_data)
        # for i in range(0,len(timelist)):
        #print("Time: %s  Type: %s PS: %s " % (timelist[i],gdtypelist[i],psnamelist[i]))
        for i in range(0, len(timelist)):
            if Get_querter(int(timelist[i].hour)) == qtr:
                timelistX.append(timelist[i])
                gdtypelistX.append(gdtypelist[i])
                psnamelistX.append(psnamelist[i])
        gdFreq = CountFrequency(gdtypelistX)
        psFreq = CountFrequency(psnamelistX)
        if(len(count) == 0):
            crime_rate_perCountry = 0
        else:
            crime_rate_perCountry = len(timelist)/len(count)*100

        if (len(timelist) == 0):
            crime_rate_perArea = 0
        else:
            crime_rate_perArea = len(timelistX)/len(timelist)*100
        # print(gdFreq)

        # for i in range(0,len(timelistX)):
            #print("Time: %s  Type: %s PS: %s " % (timelistX[i],gdtypelistX[i],psnamelistX[i]))

    qs = GeneralDiary.objects.all().values(
        'issuedate', 'issuetime', 'gdtype', 'psname', 'area')
    data = pd.DataFrame(qs)
    Dist_data = AreaName.objects.all().order_by('district')
    context = {'data': data.to_html(), 'describe': data.describe(
    ).to_html(), 'Dist_data': Dist_data, 'psfreq': psFreq, 'gdfreq': gdFreq, 'crime_rate_area': int(crime_rate_perArea),
        'crime_rate_country': int(crime_rate_perCountry), 'area': area, 'time': inputtime, 'qtr': qtr}
    return render(request, 'prediction.html/', context)
