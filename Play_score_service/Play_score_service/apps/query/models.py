# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Score(models.Model):
    users = models.CharField(verbose_name='客户端号', max_length=16, unique=True)
    score = models.IntegerField(verbose_name='分数', default=0, validators=[MaxValueValidator(10000000), MinValueValidator(1)])

    class Meta:
        db_table = 'tb_score'
        verbose_name = '分数'
        verbose_name_plural = verbose_name


class Rank(models.Model):
    u_id = models.OneToOneField(Score, on_delete=models.CASCADE, primary_key=True, )
    rank = models.IntegerField(verbose_name='名次', validators=[MinValueValidator(1)])




