from django.http import JsonResponse
from django.shortcuts import render

from .models import Branch, Mileage, Train


def get_context():
    context = {
        'branches': Branch.objects.all(),
        'trains': Train.objects.all(),
        'years': tuple(item['year'] for item in Mileage.objects.values('year').distinct())
    }
    data = []
    for branch in Branch.objects.all():
        data.append(
            {
                'id': branch.id,
                'text': branch.name,
                'children': [
                    {
                        'id': f'{branch.id}_{train.id}',
                        'text': train.name,
                        'name': f'{branch.name}:{train.name}'
                    } for train in branch.trains.all()
                ]
            }
        )
    context['loko_data'] = data
    return context


def index(request):
    return render(request, 'ldata/index.html', context=get_context())


def calc(request):
    query = request.GET['lquery']
    year_from = request.GET['yearfrom']
    year_to = request.GET['yearto']
    query = Mileage.objects.get_stats(lquery=query, year_from=year_from, year_to=year_to)
    years, totals = [], []
    for item in query.all():
        years.append(item['year'])
        totals.append('{0:.2f}'.format(item['total']))
    return JsonResponse({'labels': years, 'data': totals})
