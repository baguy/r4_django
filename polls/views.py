from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sessions.models import Session

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    if request.method == 'POST':
        all_sessions = Session.objects.all()

        if 'sessionid' in request.COOKIES:
            cookie = request.COOKIES['sessionid']
        else:
            cookie = 'a'

        first_vote = True
        for session in all_sessions:
            if cookie == str(session):
                first_vote = False
                context = {
                    'fist_vote': first_vote,
                }
                return render(request, 'polls/message.html', context)
            else:
                question = get_object_or_404(Question, pk=question_id)
                try:
                    selected_choice = question.choice_set.get(pk=request.POST['choice'])
                    question.total += 1
                except (KeyError, Choice.DoesNotExist):
                    # Redisplay the question voting form.
                    return render(request, 'polls/detail.html', {
                        'question': question,
                        'error_message': "You didn't select a choice.",
                    })
                else:
                    selected_choice.votes += 1
                    selected_choice.save()
                    question.save()
                    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    all_choices = Choice.objects.all()
    labels = []
    votes = []
    for choice in all_choices:
        if choice.question_id == question_id:
            labels.append(choice.choice_text)
            votes.append(choice.votes)

    context = {
        'question': question,
        'votes': json.dumps(votes),
        'labels': json.dumps(labels)
    }

    return render(request, 'polls/results.html', context)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer