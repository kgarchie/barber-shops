import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, AppointmentsCreationForm
from django.contrib.auth.models import User
from .models import Barber, Locations, Appointments, Cut, Reports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient

stk_push_callback_url = 'https://darajambili.herokuapp.com/express-payment'
b2c_callback_url = 'https://darajambili.herokuapp.com/b2c/result'

cl = MpesaClient()


# Create your views here.

class Phone:
    phone = ''


def index(request):
    return render(request, 'index.html')


@login_required(login_url='app:login')
def book(request):
    form = AppointmentsCreationForm()
    barbers = Barber.objects.all().filter(available=True)
    locales = Locations.objects.all()
    cuts = Cut.objects.all()
    context = {
        'barbers': barbers,
        'cuts': cuts,
        'locales': locales,
        'form': form,
    }
    if request.method == 'POST':
        user = request.user
        cut_f = request.POST['cut']
        if cut_f != '':
            cut = Cut.objects.get(id=cut_f)
        else:
            cut = Cut.objects.get(id=1)
        barber_f = request.POST['barber']
        if barber_f != '':
            barber = Barber.objects.get(id=barber_f)
        else:
            barber = Barber.objects.get(id=1)

        dye = False

        phone_number = request.POST['phone']
        sth = request.POST['sth']
        locale_f = request.POST['locale']
        if locale_f != '':
            locale = Locations.objects.get(id=locale_f)
        else:
            locale = Locations.objects.get(id=1)
        print('Filled Everything')
        appointment = Appointments.objects.create(user=user, cut=cut, barber=barber, dye=dye, sth=sth, locale=locale)
        record_report(user, appointment)
        if phone_number:
            Phone.phone = phone_number
            return redirect('app:force-pay')
        return redirect('app:appointments')
    return render(request, 'bookings.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('app:home')
        else:
            context = {
                'errors': "User does not exist",
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('app:login')


def register(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            if user is not None:
                User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('app:home')
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='app:login')
def appointments(request):
    appointment = Appointments.objects.filter(user=request.user)
    context = {
        'appointments': appointment,
    }
    if 'next' in request.POST:
        return redirect(request.POST['next'])

    return render(request, 'success.html', context)


def about(request):
    return render(request, 'about.html')


def cs(request):
    return render(request, 'cs.html')


def record_report(user, appointment):
    report = Reports.objects.create(user=user)
    report.appointments.add(appointment)

    print('Recorded')


def get_reports(request):
    if request.user.is_staff:
        reports = Reports.objects.all()
        report_appointments = []
        context = {
            'reports': reports,
            'appointment': report_appointments,
        }
        return render(request, 'reports.html', context)


def get_report_details(request, id):
    if request.user.is_staff:
        user = Reports.objects.get(id=id).user
        appointment = Appointments.objects.filter(user=user)
        context = {
            'appointments': appointment,
        }

        return render(request, 'report-details.html', context)


def stk_push_callback(request):
    data = request.body
    message = data["ResultDesc"]

    appointment = Appointments.objects.filter(user=request.user)
    context = {
        'appointments': appointment,
        'message': message,
    }

    return render(request, 'success.html', context)
    # You can do whatever you want with the notification received from MPESA here.


def oauth_access(request):
    return JsonResponse(cl.access_token(), safe=False)


def stk_push_success(request):
    phone_number = Phone.phone
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    # callback_url = stk_push_callback_url # use when unhosted
    # This url is to be used only when the site is hosted on an online server
    callback_url = request.build_absolute_uri(reverse('app:mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    # return HttpResponse(response)
    return redirect('app:mpesa_stk_push_callback')


def business_payment_success(request):
    pass
