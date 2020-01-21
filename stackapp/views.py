from django.shortcuts import render, HttpResponse
from .utils import StackAPIConsumer, StackAPIQuestion
from .forms import StackAPIConsumerForm


def test(request):
    if request.method == 'GET':
        form = StackAPIConsumerForm
        args = {'form': form}
        return render(request, 'stackapp/test.html', args)
    else:
        form = StackAPIConsumerForm(request.POST or None)
        if form.is_valid():
            res = StackAPIConsumer.consume(form.cleaned_data)

            data = []
            for response in res.json()['items']:
                data.append(StackAPIQuestion(response))
            print(data)
            args = {'response': data}
            return render(request, 'stackapp/result.html', args)
