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
                    }  for train in branch.trains.all()
                ]
                # 'children': [{'id': '228', 'name': 'qool', 'text':'aaa'},{'id':'229','name': 'qooxl', 'text':'bbb'}]
            }
        )
    context['loko_data'] = data
    # context['loko_data'] = [
    #         {
    #             'id': '',
    #             'text': 'Citrus',
    #             'children': [
    #                 { 'id': 'c1', 'text': 'Grapefruit' },
    #                 { 'id': 'c2', 'text': 'Orange' },
    #                 { 'id': 'c3', 'text': 'Lemon' },
    #                 { 'id': 'c4', 'text': 'Lime' }
    #             ]
    #         },
    #         {
    #             'id': '',
    #             'text': 'Other',
    #             'children': [
    #                 { 'id': 'o1', 'text': 'Apple' },
    #                 { 'id': 'o2', 'text': 'Mango' },
    #                 { 'id': 'o3', 'text': 'Banana' }
    #             ]
    #         }
    #     ]
    return context


def index(request):
    return render(request, 'ldata/index.html', context=get_context())
    # return HttpResponse('hi!')


def calc(request):
    context = get_context()
    context['branch'] = request.GET['branch']
    context['train'] = request.GET['train']
    context['kmfrom'] = request.GET['kmfrom']
    context['kmto'] = request.GET['kmto']
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
