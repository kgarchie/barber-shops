import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import base64
from requests.auth import HTTPBasicAuth

from .forms import UserCreationForm, AppointmentsCreationForm
from django.contrib.auth.models import User
from .models import Barber, Locations, Appointments, Cut
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponse
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient

stk_push_callback_url = 'https://darajambili.herokuapp.com/express-payment'
b2c_callback_url = 'https://darajambili.herokuapp.com/b2c/result'


# Create your views here.

def index(request):
    return render(requests, 'index.html')


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

        phone = request.POST['phone']
        if phone:
            # lipa_na_mpesa_online(phone)
            LipaV_2(request, phone)
        sth = request.POST['sth']
        locale_f = request.POST['locale']
        if locale_f != '':
            locale = Locations.objects.get(id=locale_f)
        else:
            locale = Locations.objects.get(id=1)
        print('Filled Everything')
        Appointments.objects.create(user=user, cut=cut, barber=barber, dye=dye, sth=sth, locale=locale)
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
    count = Appointments.objects.all().count()
    context = {
        'appointments': appointment,
        'count': count,
    }
    if 'next' in request.POST:
        return redirect(request.POST['next'])

    return render(request, 'success.html', context)


def about(request):
    return render(request, 'about.html')


def cs(request):
    return render(request, 'cs.html')


# Deprecated
def get_mpesa_token():
    consumer_key = "AwAmK7Uv7SsKc2ETzNEtaCS3glvl5phV"
    consumer_secret = "aU6I2DibjXpyfh2f"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # make a get request using python requests library
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # return access_token from response
    token = r.json()['access_token']

    return token


# Deprecated
class LipanaMpesaPassword:
    lipa_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')


# Deprecated
def lipa_na_mpesa_online(phone):
    access_token = get_mpesa_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
        "Password": LipanaMpesaPassword.decode_password,
        "Timestamp": LipanaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPassword.Business_short_code,
        "PhoneNumber": phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Abdi",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    print(str(response))
    return HttpResponse(str(response))


def LipaV_2(request, phone):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = phone
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = request.build_absolute_uri(
        reverse('app:mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount,
                           account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


def stk_push_callback(request):
    data = request.body
    print(data)
    return render(request, 'success.html')
    # You can do whatever you want with the notification received from MPESA here.
