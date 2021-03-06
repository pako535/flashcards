from django import forms
from .models import Words


class Switch(forms.Form):
    CHOICES = [('pl', 'Polski'),
               ('eng', 'Angielski')]
    
    switch = forms.ChoiceField(
        label="Wybierz język wpisywania słów: ",
        choices=CHOICES,
        widget=forms.RadioSelect())


class TestYourSelf(forms.Form):
    translate = forms.CharField(
        label='Tłumaczenie: ',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'inputs',
                                      'autocomplete': 'off'}))


class AddWords(forms.Form):
    pl_word = forms.CharField(
        label='Po polsku: ',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'inputs',
                                      'autocomplete': 'off'}))
    
    eng_word = forms.CharField(
        label='Po angielsku: ',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'inputs',
                                      'autocomplete': 'off'}))


class Login(forms.Form):
    login = forms.CharField(
        label='Login: ',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'inputs',
                                      'autocomplete': 'off'}))
    
    password = forms.CharField(
        label='Hasło: ',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'inputs',
                                      'autocomplete': 'off'}))
