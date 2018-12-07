from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Words, MyUser
from .forms import AddWords, TestYourSelf, Login
from random import choice


# Create your views here.

@csrf_exempt
def main(request):
    if request.method == 'POST':
        form = Login(request.POST)
        print(form.errors)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = MyUser.objects.filter(login=cleaned_data['login'], password=cleaned_data['password']).first()
            if user:
                request.session['user'] = user.id
                return render(request, 'main.html')
            else:
                return render(request, 'mess.html', {'mess': 'Podaj prawidłowe hasło i login'})
    elif request.method == 'GET':
        form = Login()
        return render(request, 'login_or_register.html', {'form': form})
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def add_word(request):
    if request.method == 'POST':
        form = AddWords(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            tmp = Words(
                pl_word=cleaned_data['pl_word'].upper(),
                eng_word=cleaned_data['eng_word'].upper(),
                user=MyUser.objects.filter(id=request.session['user']).first(),
            )
            tmp.save()
            return render(request, 'main.html')
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
        tmp_list = Words.objects.filter(user__id=request.session['user'])
        if not tmp_list:
            return render(request, "mess.html", {'mess': 'Brak słówek. Dodaj słówka'})
        tmp_list = [x for x in tmp_list if x.counter <= 3]
        random_words = choice(tmp_list)
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


def reset(request):
    if request.method == 'POST':
        for x in Words.objects.filter(user=request.session['user']):
            x.counter = 0
            x.save()
        return render(request, 'main.html')


def check_words(request, cleaned_data):
    if request.session['lang']:
        word = Words.objects.filter(pl_word=request.session['random'],
                                    eng_word=cleaned_data['translate'].upper()).first()
        if word:
            word.counter = word.counter + 1
            word.save()
            return True
        else:
            return False
    else:
        word = Words.objects.filter(pl_word=cleaned_data['translate'].upper(),
                                    eng_word=request.session['random']).first()
        if word:
            word.counter = word.counter + 1
            word.save()
            return True
        else:
            return False


def get_words(request, cleaned_data):
    if request.session['lang']:
        tmp = Words.objects.filter(pl_word=request.session['random'])
        if tmp:
            return tmp
    else:
        tmp = Words.objects.filter(eng_word=request.session['random'])
        if tmp:
            return tmp
