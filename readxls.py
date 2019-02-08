import xlrd
from django.db import transaction
from ldata.models import Branch, Mileage, Train

book = xlrd.open_workbook('test_LT.xlsx')


@transaction.atomic
def read_branches():
    branch = book.sheet_by_index(3)
    for rx in range(branch.nrows):
        item, = [branch.cell_value(rx, rc) for rc in range(branch.ncols)]
        print('Branch', item)
        b = Branch(name=item)
        b.save()
        print(b)


@transaction.atomic
def read_prirces():
    prices = book.sheet_by_index(2)
    for rx in range(1, prices.nrows):
        brand, price = [prices.cell_value(rx, rc) for rc in range(prices.ncols)]
        print('b, p', brand, price)
        t = Train(name=brand, price=price)
        t.save()
        print(t)


@transaction.atomic
def read_mileage():
    runs = book.sheet_by_index(1)
    year_label = [int(runs.cell_value(0, c)) for c in range(2, runs.ncols)]
    for rx in range(1, runs.nrows):
        branch, brand, *years = [runs.cell_value(rx, rc) for rc in range(runs.ncols)]
        years = {label: y for label, y in zip(year_label, years)}
        print(branch, brand, years)
        branch = Branch.objects.get(name=branch)
        train = Train.objects.get(name=brand)
        branch.trains.add(train)
        branch.save()
        for year, km in years.items():
            m = Mileage(branch=branch, train=train, year=year, km=km)
            m.save()
            print(m)


read_branches()
read_prirces()
read_mileage()
