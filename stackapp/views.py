from django.shortcuts import render, HttpResponse
from .utils import StackAPIConsumer
from .forms import StackAPIConsumerForm


def test(request):
    if request.method == 'GET':
        form = StackAPIConsumerForm
        args = {'form': form}
        return render(request, 'stackapp/test.html', args)
    else:
        form = StackAPIConsumerForm(request.POST or None)
        if form.is_valid():
            StackAPIConsumer.consume(form.cleaned_data)
            return HttpResponse(form.cleaned_data)
