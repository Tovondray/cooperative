from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Compte créé pour {user.username} ! Connectez-vous.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'comptes/register.html', {'form': form})








def login_view(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect("dashboard")

            else:

                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, "login.html", {"form": form})