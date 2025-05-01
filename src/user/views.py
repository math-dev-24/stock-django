from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserCreationForm, UserLoginForm


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bonjour {user.username}, vous êtes maintenant connecté.')
            return redirect('stock:dashboard')
        else:
            return render(request, 'user/login.html', context={'form': form})

    form = UserLoginForm()
    return render(request, 'user/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes maintenant déconnecté.")
    return redirect('stock:home')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            messages.success(request, f'Compte créé avec succès pour {user.username}! Vous êtes maintenant connecté.')
            return redirect('stock:home')
        else:
            return render(request, 'user/register.html', context={'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'user/register.html', context={'form': form})


@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'user/account.html', context)