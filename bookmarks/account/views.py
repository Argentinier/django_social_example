from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.forms import LoginForm


def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is None:
                return HttpResponse('Invalid Login. User or Password is not correct.')

            if not user.is_active:
                return HttpResponse('Account is disabled.')

            login(request, user)
            return HttpResponse('Authenticated successfully!')

    return render(
        request=request,
        template_name='account/login.html',
        context={'form': form}
    )
