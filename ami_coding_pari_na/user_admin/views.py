from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.utils.encoding import force_str
from django.contrib.auth.models import Group
from .models import User
from .forms import createuserform, Permissionform
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
# Create your views here.



def ActivateAccount(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, ('Your account have been confirmed.'))
        return redirect('home')
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('home')



def user_registration(request):
    context={}
    forms = createuserform()
    context['forms'] = forms
    if request.POST:
        forms = createuserform(request.POST)
        if forms.is_valid():
            password = forms.cleaned_data['password']
            user = forms.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.set_password(password)
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your School Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = forms.cleaned_data.get('email')
            send_mail(subject, message, 'mailzahidul@gmail.com', [to_email])
            # user.email_user(subject, message)
            messages.success(request, ('Please Confirm your email to complete registration.'))
            return redirect('login')
        else:
            messages.error(request, forms.errors)
        return render(request, 'user/registration.html', context)
    return render(request, 'user/registration.html', context)


def user_login(request):
    if request.POST:
        email = request.POST['email_id']
        password = request.POST['password']
        try:
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email or password incorrect.')
        except Exception as err:
            print(err)
    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

