from django.shortcuts import redirect, render
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from .forms import ContactUs
from django.core.mail import send_mail
from django.contrib import messages
from .models import Banner, Section
from .forms import SignupForm, ProfileForm
from django.contrib.auth import authenticate, login


def home(request):
    banners = Banner.objects.all()
    sections = Section.objects.all()
    form = ContactUs()
    if request.method == 'POST':
        form = ContactUs(request.POST)
        from_name = str(form['name'].value())
        from_email = str(form['email'].value())
        subject = str(form['subject'].value())
        message = str(form['message'].value()) + \
            f'\nfrom :name: {from_name} email: {from_email}'

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email,
                          ['f.benayad95@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(
                request, f'Your email has been sent successfully to Company')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

    context = {
        'title': 'Home',
        'banners': banners,
        'sections': sections,
        'form': form
    }
    return render(request, 'main/home.html', context)


# SignUp
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('main:home')
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})


# Edit Profile
def edit_profile(request):
    msg = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Data has been saved'
    form = ProfileForm(instance=request.user)
    return render(request, 'registration/edit-profile.html', {'form': form, 'msg': msg})
