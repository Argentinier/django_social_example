from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from account import forms
from account.forms import UserEditForm, ProfileEditForm
from account.models import Profile


@login_required
def dashboard(request):
    return render(
        request=request,
        template_name='account/dashboard.html',
        context={'section': 'dashboard'})


def user_registration(request):
    form = forms.UserRegistrationForm()

    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)

        if form.is_valid():
            user: User = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Creates a new empty Profile for this user.
            Profile.objects.create(user=user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': user})

    return render(request,
                  'account/register.html',
                  {'user_form': form})


@login_required()
def edit(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request=request, message='Your Profile information was saved successfully!')
        else:
            messages.error(request=request, message='Fail to update information. Check the form fields error messages.')

    return render(
        request=request,
        template_name='account/edit.html',
        context={
            'user_form': user_form,
            'profile_form': profile_form
        })


# def user_login(request):
#     form = LoginForm()
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(request, username=data['username'], password=data['password'])
#
#             if user is None:
#                 return HttpResponse('Invalid Login. User or Password is not correct.')
#
#             if not user.is_active:
#                 return HttpResponse('Account is disabled.')
#
#             login(request, user)
#             return HttpResponse('Authenticated successfully!')
#
#     return render(
#         request=request,
#         template_name='account/login.html',
#         context={'form': form}
#     )
