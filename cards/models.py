from django.db import models


# Create your models here.

class MyUser(models.Model):
    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'
    
    login = models.CharField(max_length=100, unique=True, verbose_name="Login")
    password = models.CharField(max_length=100, verbose_name="Hasło")
    
    def __str__(self):
        return "{} {}".format(self.id, self.login)


class Words(models.Model):
    class Meta:
        verbose_name = 'Słowo'
        verbose_name_plural = 'Słówka'
    
    pl_word = models.CharField(max_length=100, verbose_name="Po polsku")
    eng_word = models.CharField(max_length=100, verbose_name="Po angielsku")
    user = models.ForeignKey(MyUser, on_delete=None)
    counter = models.IntegerField(verbose_name="Licznik", default=0)
    
    def __str__(self):
        return "{} -> {}".format(self.pl_word, self.eng_word)
