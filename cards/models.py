from django.db import models


# Create your models here.

class Words(models.Model):
    class Meta:
        verbose_name = 'Słowo'
        verbose_name_plural = 'Słówka'
    
    pl_word = models.CharField(max_length = 100, verbose_name = "Po polsku")
    eng_word = models.CharField(max_length = 100, verbose_name = "Po angielsku")
    
    def __str__(self):
        return "{} -> {}".format(self.pl_word, self.eng_word)

