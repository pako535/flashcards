from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Words
from .forms import AddWords, TestYourSelf
from random import choice


# Create your views here.

@csrf_exempt
def main(request):
    return render(request, 'main.html')

@csrf_exempt
def add_word(request):
    if request.method == 'POST':
        form = AddWords(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            tmp = Words(
                pl_word = cleaned_data['pl_word'].upper(),
                eng_word = cleaned_data['eng_word'].upper()
            )
            tmp.save()
            return render(request, 'mess.html')
        return render(request, 'add_word.html', {'form': form})
    elif request.method == 'GET':
        form = AddWords()
        return render(request, 'add_word.html', {'form': form})
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def learn(request):
    if request.method == 'POST':
        form = TestYourSelf(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            if check_words(request, cleaned_data):
                return redirect('/learn')
            else:
                tmp = get_words(request, cleaned_data)
                tmp = tmp.first()
                pl = tmp.pl_word
                eng = tmp.eng_word
                return render(request, 'false.html', {'pl': pl,
                                                      'eng': eng})
        
        return render(request, 'learn.html', {'form': form})
    elif request.method == 'GET':
        form = TestYourSelf()
        random_words = choice(Words.objects.all())
        tmp = [random_words.pl_word, random_words.eng_word]
        random_word = choice(tmp)
        random_word = str(random_word)
        request.session['random'] = random_word
        
        if random_word == random_words.pl_word:
            request.session['lang'] = True
        elif random_word == random_words.eng_word:
            request.session['lang'] = False
        
        return render(request, 'learn.html', {'form': form,
                                              'random': random_word})
    else:
        return HttpResponseBadRequest()


def check_words(request, cleaned_data):
    if request.session['lang']:
        if Words.objects.filter(pl_word = request.session['random'], eng_word = cleaned_data['translate'].upper()):
            return True
        else:
            return False
    else:
        if Words.objects.filter(pl_word = cleaned_data['translate'].upper(), eng_word = request.session['random']):
            return True
        else:
            return False

def get_words(request, cleaned_data):
    if request.session['lang']:
        tmp = Words.objects.filter(pl_word = request.session['random'])
        if tmp:
            return tmp
    else:
        tmp = Words.objects.filter(eng_word = request.session['random'])
        if tmp:
            return tmp
