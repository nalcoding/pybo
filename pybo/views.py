from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    # 입력인자
    page = request.GET.get('page', '1')

    #조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10) #페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj}
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다")


    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(id=
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(content=request.POST.get('content'),create_date=timezone.now())
    # return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        print('(Post) AnswerForm')
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
        print('(GET) AnswerForm')

    context = {'question':question, 'form':form}
    print('Answer context : \n ',context)
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST) ## 여기 form if 문 안에서만 존재하는 지역변수
        print("Post Form : ", form)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() ## 여기 form 은 else 안에만 존재하는 지역변수
        print("Get Form : ", form)
    context = {'form': form} ## if 문 밖에 정의된 form에 값이 들어가는 원리가 이해가 되지 않음...

    return render(request, 'pybo/question_form.html', context)