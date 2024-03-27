from django.shortcuts import get_object_or_404, render # get_object_or_404 : 장고의 단축함수
#추가
from polls.models import Choice, Question
# 추가(p 140)
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html',context)

# p 138 3-9
# 뷰함수 정의 (URL패턴에서 추출된 question_id 파라미터라 뷰함수 인자로 넘어옴)
def detail(request, question_id): # request: 필수인자
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{'question':question})

# p 140 3-10
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여준다.
        return render(request, 'polls/detail.html',{
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        # POST 데이터를 정상적으로 처리하였으면,
        # 항상 HttpResponseRedirect를 반한하여 리다이렉션 ㅊ러ㅣ함
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

# p 143 3-11
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html',{'question':question})