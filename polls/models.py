import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    total = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(self, request, args, kwargs)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text