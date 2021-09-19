from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    logged_in = request.user.is_authenticated
    if request.method == 'POST' and not logged_in:
        first_name = request.POST['first_name']
        last_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'That email is already being used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email,
                first_name=first_name, last_name=last_name)
                # auth.login(request, user)
                # messages.success(request, "You are now logged in")
                user.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login') 
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    if logged_in:
        return redirect('dashboard')
    return render(request, 'accounts/register.html')

def login(request):
    logged_in = request.user.is_authenticated
    if request.method == 'POST' and not logged_in:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    if logged_in:
        return redirect('dashboard')
    return render(request, 'accounts/login.html')

def logout(request):
    logged_in = request.user.is_authenticated
    if request.method == 'POST' and logged_in:
        auth.logout(request)
        messages.success(request,'You are now logged out')
    return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
