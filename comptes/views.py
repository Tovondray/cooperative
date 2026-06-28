from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

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