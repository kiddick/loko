from django.http import HttpResponse
from django.shortcuts import render

from .models import Branch, Mileage, Train


def get_context():
    context = {
        'branches': Branch.objects.all(),
        'trains': Train.objects.all(),
        'kms': tuple(item['year'] for item in Mileage.objects.values('year').distinct())
    }
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

# На основе приложенных данных (test_LT.xlsx) сделать мини-сервис, предоставляющий возможность выводить график суммарной выручки по годам.
# Реализовать возможность фильтровать результаты по филиалу, серии локомотива и периоду.
# Выручка = пробег * ставка
#
# Сервис должен состоять из одной страницы, на которой есть:
#   -форма с возможностью выбора филиала, серии локомотива и периода
#   -график, отображающий выручку по годам в соответствии с заданными в форме параметрами (в срезе по филиалу и/или по серии)
# Желательно сделать так, чтобы при сабмите формы отправлялся ajax-запрос, и график перестраивался без перезагрузки всей страницы.
#
# Стили и клиентские библиотеки для интерактивных полей формы и графиков нужно взять из открытого шаблона https://adminlte.io
# Бэкенд должен быть реализован на django, python 3.4
#
# Желательно написать в readme, как поднять проект.