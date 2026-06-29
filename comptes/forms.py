from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClientProfile, CooperativeProfile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect, label="Type de compte")
    telephone = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=True)

    # Champs coopérative
    nom_cooperative = forms.CharField(max_length=100, required=False, label="Nom de la coopérative")
    adresse_cooperative = forms.CharField(widget=forms.Textarea, required=False, label="Adresse de la coopérative")
    telephone_cooperative = forms.CharField(max_length=20, required=False, label="Téléphone de la coopérative")
    email_cooperative = forms.EmailField(required=False, label="Email de la coopérative")

    # Champs client
    adresse_client = forms.CharField(widget=forms.Textarea, required=False, label="Adresse")
    date_naissance = forms.DateField(required=False, label="Date de naissance", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'password1', 'password2', 'role']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'cooperative':
            if not cleaned_data.get('nom_cooperative'):
                self.add_error('nom_cooperative', 'Ce champ est obligatoire pour une coopérative.')
            if not cleaned_data.get('adresse_cooperative'):
                self.add_error('adresse_cooperative', 'Ce champ est obligatoire pour une coopérative.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.telephone = self.cleaned_data['telephone']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if user.role == 'client':
                ClientProfile.objects.create(
                    user=user,
                    adresse=self.cleaned_data.get('adresse_client', ''),
                    date_naissance=self.cleaned_data.get('date_naissance', None)
                )
            elif user.role == 'cooperative':
                CooperativeProfile.objects.create(
                    user=user,
                    nom_cooperative=self.cleaned_data['nom_cooperative'],
                    adresse=self.cleaned_data['adresse_cooperative'],
                    telephone=self.cleaned_data['telephone_cooperative'],
                    email=self.cleaned_data['email_cooperative'],
                    est_validee=False
                )
        return use






class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Entrez votre nom",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "••••••••",
            "class": "form-control",
            "id": "id_password"
        })
    )