from django.shortcuts import render, HttpResponse
from .utils import StackAPIConsumer, StackAPIQuestion
from .forms import StackAPIConsumerForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
from datetime import datetime, timedelta


def test(request):
    if request.method == 'GET':
        form = StackAPIConsumerForm(request.GET or None)
        day_time = request.session.get('day_time')
        minute_time = request.session.get('minute_time')
        search_number = request.session.get('searches')
        url = request.get_full_path()
        if search_number is None:
            search_number = 0
        if day_time is None:
            milliseconds = int(round(datetime.now().timestamp() * 1000))
            day_time = request.session['day_time'] = milliseconds
        if minute_time is None:
            milliseconds = int(round(datetime.now().timestamp() * 1000))
            minute_time = request.session['minute_time'] = milliseconds

        minute_time = datetime.fromtimestamp(minute_time / 1000.0)
        day_time = datetime.fromtimestamp(day_time / 1000.0)
        minutes_delta = timedelta(minutes=1)
        day_delta = timedelta(days=1)
        now_time = datetime.now()

        if ((now_time - minute_time) < minutes_delta and search_number >= 5) \
                or \
                ((now_time - day_time) < day_delta and search_number >= 100):
            return HttpResponse("you have passed the amount of sessions you can have")
        if (now_time - minute_time) > minutes_delta:
            request.session['minute_time'] = None
            search_number = 0
        if (now_time - day_time) > day_delta:
            request.session['day_time'] = None
            search_number = 0

        if form.is_valid():
            res = cache.get(request.get_full_path())
            if res is None:
                res = StackAPIConsumer.consume(form.cleaned_data)
                cache.set(request.get_full_path(), res)
            data = []
            for response in res.json()['items']:
                data.append(StackAPIQuestion(response))
            search_number += 1
            request.session['searches'] = search_number
            page = request.GET.get('the_page', 1)
            paginator = Paginator(data, 10)
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)

            args = {'response': data, 'url': url}
            return render(request, 'stackapp/test.html', args)
        args = {'form': form}
        return render(request, 'stackapp/test.html', args)
