from django.http import HttpResponse
from django.shortcuts import render

from .models import Branch, Mileage, Train


def get_context():
    context = {
        'branches': Branch.objects.all(),
        'trains': Train.objects.all(),
        'kms': tuple(item['year'] for item in Mileage.objects.values('year').distinct())
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
                # 'children': [{'id': '228', 'name': 'qool', 'text':'aaa'},{'id':'229','name': 'qooxl', 'text':'bbb'}]
            }
        )
    context['loko_data'] = data
    return context


def index(request):
    return render(request, 'ldata/index.html', context=get_context())
    # return HttpResponse('hi!')


def calc(request):
    context = get_context()
    query = request.GET['lquery']
    year_from = request.GET['kmfrom']
    year_to =  request.GET['kmto']
    context['lquery'] = query
    context['kmfrom'] = year_from
    context['kmto'] = year_to
    q = Mileage.objects.get_stats(query=query, year_from=year_from, year_to=year_to)
    print('count:', q)
    # print('q:', q.query)
    # print('count:', q.count())
    years = []
    totals = []
    for i in q.all():
        years.append(i['year'])
        totals.append(i['total'])
    # {
    #     labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    #     datasets: [{
    #         label: 'BaBLO$$',
    #         data: [12, 19, 3, 5, 2, 3],
    #         borderWidth: 1
    #     }]
    # }
    chart = {
        'labels': years,
        'datasets': [{
            'label': 'BaBLO$$',
            'data': totals,
            'borderWidth': 1
        }]}
    print(chart)
    context['chart'] = chart
    return render(request, 'ldata/index.html', context=context)

# На основе приложенных данных (test_LT.xlsx) сделать мини-сервис, предоставляющий возможность выводить график
# суммарной выручки по годам.
# Реализовать возможность фильтровать результаты по филиалу, серии локомотива и периоду.
# Выручка = пробег * ставка
#
# Сервис должен состоять из одной страницы, на которой есть:
#   -форма с возможностью выбора филиала, серии локомотива и периода
#   -график, отображающий выручку по годам в соответствии с заданными в форме параметрами (в срезе по филиалу и/или
#   по серии)
# Желательно сделать так, чтобы при сабмите формы отправлялся ajax-запрос, и график перестраивался без перезагрузки
# всей страницы.
#
# Стили и клиентские библиотеки для интерактивных полей формы и графиков нужно взять из открытого шаблона
# https://adminlte.io
# Бэкенд должен быть реализован на django, python 3.4
#
# Желательно написать в readme, как поднять проект.
