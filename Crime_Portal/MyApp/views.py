from django.shortcuts import render, redirect
from MyApp.userdetails import User
from django.contrib import messages
from MyApp.models import Authentication, Registered_Users, WantedCriminals, AreaName, PSNames, GeneralDiary, GeneralDiaryByUsers, CrimeNews, LocalIntelligence
import random

obj = User()


def home(request):
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
    return render(request, 'aboutus.html/')


def crimenews(request):
    data = CrimeNews.objects.all().order_by('-date')
    return render(request, 'crimenews.html/', {'data': data})


def localintelligence(request):
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


def violencereporting(request):
    return render(request, 'violencereporting.html/')


def wantedlist(request):
    if request.method == 'GET':
        data = WantedCriminals.objects.all().order_by('name')
        return render(request, 'wantedlist.html/', {'data': data})


def userDashboard(request):
    value = obj.get_name()
    data = Registered_Users.objects.all().filter(email=value)
    # print(data)
    return render(request, 'userDashboard.html/', {'data': data})


def gd(request):
    if request.method == 'GET':
        Dist_data = AreaName.objects.all().order_by('district')
        PS_data = PSNames.objects.all().order_by('psname')
        return render(request, 'gd.html/', {'Dist_data': Dist_data, 'PS_data': PS_data})
    if request.method == 'POST':
        value = obj.get_name()
        userDataList = Registered_Users.objects.all().filter(email=value).values_list()
        # print(userDataList)
        for element in userDataList:
            email = element[1]
            name = element[2]+element[3]
            nid = element[5]
        mobile = request.POST['mobile']
        issuedate = request.POST['datetime']
        gdtype = request.POST['gdtype']
        area = request.POST['area']
        psname = request.POST['psname']
        subject = request.POST['gdsubject']
        details = request.POST['gddetails']
        gd_id = random.randint(0, 3000)

        GD_Creation_queryset = GeneralDiary(email=email, nid=nid, name=name, mobile=mobile, issuedate=issuedate,
                                            gdtype=gdtype, area=area, psname=psname, subject=subject, details=details, gd_id=gd_id)
        GD_Record_command = GeneralDiaryByUsers(
            email=email, gd_id=gd_id, creation_date_time=issuedate)

        GD_Creation_queryset.save()
        GD_Record_command.save()
        return redirect('/gd.html/')
