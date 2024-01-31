from django.shortcuts import render, redirect
from .models import Memo
from .forms import MemoForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import datetime
def index(request):
  memos = Memo.objects.all().order_by('-updated_datetime')
  dt_now =  datetime.date.today()
  return render(request, 'memoApp/index.html', { 'memos': memos,'dt_now':dt_now })

def detail(request, memo_id):
  memo = get_object_or_404(Memo, id=memo_id)
  return render(request, 'memoApp/detail.html', {'memo': memo})

def new_memo(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('memoApp:index')
    else:   
        form = MemoForm
    return render(request, 'memoApp/new_memo.html', {'form': form })

@require_POST
def delete_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id)
    memo.delete()
    return redirect('memoApp:index')

def edit_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memoApp:index')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memoApp/edit_memo.html', {'form': form, 'memo':memo })
