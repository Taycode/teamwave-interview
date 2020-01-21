from django.shortcuts import render, HttpResponse
from .utils import StackAPIConsumer, StackAPIQuestion
from .forms import StackAPIConsumerForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache


def test(request):
    if request.method == 'GET':
        form = StackAPIConsumerForm(request.GET or None)
        if form.is_valid():
            res = cache.get(request.get_full_path())
            if res is None:
                res = StackAPIConsumer.consume(form.cleaned_data)
                cache.set(request.get_full_path(), res)
                print('mo wole')
            data = []
            for response in res.json()['items']:
                data.append(StackAPIQuestion(response))
            page = request.GET.get('the_page', 1)
            paginator = Paginator(data, 10)
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)

            args = {'response': data}
            return render(request, 'stackapp/test.html', args)
        args = {'form': form}
        return render(request, 'stackapp/test.html', args)
    # else:
    #     form = StackAPIConsumerForm(request.POST or None)
    #     if form.is_valid():
    #         res = StackAPIConsumer.consume(form.cleaned_data)
    #
    #         data = []
    #         for response in res.json()['items']:
    #             data.append(StackAPIQuestion(response))
    #         page = request.GET.get('page', 1)
    #         paginator = Paginator(data, 10)
    #         try:
    #             data = paginator.page(page)
    #         except PageNotAnInteger:
    #             data = paginator.page(1)
    #         except EmptyPage:
    #             data = paginator.page(paginator.num_pages)
    #
    #         args = {'response': data}
    #         return render(request, 'stackapp/result.html', args)
