from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, AppointmentsCreationForm
from django.contrib.auth.models import User
from .models import Barber, Locations, Appointments, Cut
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(requests):
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
        if cut_f is not '':
            cut = Cut.objects.get(id=cut_f)
        else:
            cut = Cut.objects.get(id=1)
        barber_f = request.POST['barber']
        if barber_f is not '':
            barber = Barber.objects.get(id=barber_f)
        else:
            barber = Barber.objects.get(id=1)

        dye = False

        sth = request.POST['sth']
        locale_f = request.POST['locale']
        if locale_f is not '':
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
