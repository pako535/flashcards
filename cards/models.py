from django.db import models


# Create your models here.

class Words(models.Model):
    pl_word = models.CharField(max_length = 100)
    eng_word = models.CharField(max_length = 100)
