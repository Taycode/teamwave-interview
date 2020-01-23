from django.shortcuts import render, HttpResponse
from .utils import StackAPIConsumer, StackAPIQuestion
from .forms import StackAPIConsumerForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
from datetime import datetime, timedelta


def test(request):
    if request.method == 'GET':

        # check if it is requesting for a paginated data, if it has the_page in its params
        page = request.GET.get('the_page', None)

        form = StackAPIConsumerForm(request.GET or None)

        # getting session time for minute and day limits
        day_time = request.session.get('day_time')
        minute_time = request.session.get('minute_time')

        # getting amount of searches made
        day_search_number = request.session.get('day_searches')
        minute_search_number = request.session.get('minute_searches')
        data = []
        if page is not None:
            url = request.get_full_path()[:-11]
            res = cache.get(url)
            for response in res.json()['items']:
                data.append(StackAPIQuestion(response))
        else:
            page = 1

            url = request.get_full_path()

            if day_search_number is None:
                day_search_number = 0
            if minute_search_number is None:
                minute_search_number = 0
            # convert Datetime object to millisecond and save to session
            if day_time is None:
                milliseconds = int(round(datetime.now().timestamp() * 1000))
                day_time = request.session['day_time'] = milliseconds
            if minute_time is None:
                milliseconds = int(round(datetime.now().timestamp() * 1000))
                minute_time = request.session['minute_time'] = milliseconds

            # convert back from milliseconds to datetime object

            minute_time = datetime.fromtimestamp(minute_time / 1000.0)
            day_time = datetime.fromtimestamp(day_time / 1000.0)
            minutes_delta = timedelta(minutes=1)
            day_delta = timedelta(days=1)
            now_time = datetime.now()
            print(f'day_time {day_time}')
            print(f'minute time {minute_time}')
            print(f'minute delta {now_time - minute_time}')
            print(f'day searches {day_search_number}')
            print(f'minute searches {minute_search_number}')
            # Checking if user has passed session limits
            if ((now_time - minute_time) < minutes_delta and minute_search_number >= 5) \
                    or \
                    ((now_time - day_time) < day_delta and day_search_number >= 100):
                return HttpResponse("you have passed the amount of sessions you can have")

            # resetting search number when search limit time has expired
            if (now_time - minute_time) > minutes_delta:
                request.session['minute_time'] = None
                minute_search_number = 0
            if (now_time - day_time) > day_delta:
                request.session['day_time'] = None
                day_search_number = 0

            if form.is_valid():
                res = cache.get(request.get_full_path())
                if res is None:
                    res = StackAPIConsumer.consume(form.cleaned_data)
                    cache.set(request.get_full_path(), res)
                data = []

                # return error if no data is returned based on requested parameters

                if not res.json()['items']:
                    args = {'form': form, 'error': 'There is no data gotten from this search request'}
                    return render(request, 'stackapp/test.html', args)

                for response in res.json()['items']:
                    data.append(StackAPIQuestion(response))

                day_search_number += 1
                minute_search_number += 1
                request.session['day_searches'] = day_search_number
                request.session['minute_searches'] = minute_search_number

        paginator = Paginator(data, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        # if there is data to display else return form

        if data:
            args = {'response': data, 'url': url}
            return render(request, 'stackapp/test.html', args)
        args = {'form': form}
        return render(request, 'stackapp/test.html', args)
