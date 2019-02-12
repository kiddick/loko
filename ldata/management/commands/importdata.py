import xlrd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ldata.models import Branch, Mileage, Train


@transaction.atomic
def read_branches(book):
    branch = book.sheet_by_index(3)
    for rx in range(branch.nrows):
        item, = [branch.cell_value(rx, rc) for rc in range(branch.ncols)]
        b = Branch(name=item)
        b.save()


@transaction.atomic
def read_prirces(book):
    prices = book.sheet_by_index(2)
    for rx in range(1, prices.nrows):
        brand, price = [prices.cell_value(rx, rc) for rc in range(prices.ncols)]
        t = Train(name=brand, price=price)
        t.save()


@transaction.atomic
def read_mileage(book):
    runs = book.sheet_by_index(1)
    year_label = [int(runs.cell_value(0, c)) for c in range(2, runs.ncols)]
    for rx in range(1, runs.nrows):
        branch, brand, *years = [runs.cell_value(rx, rc) for rc in range(runs.ncols)]
        years = {label: y for label, y in zip(year_label, years)}
        branch = Branch.objects.get(name=branch)
        train = Train.objects.get(name=brand)
        branch.trains.add(train)
        branch.save()
        for year, km in years.items():
            m = Mileage(branch=branch, train=train, year=year, km=km)
            m.save()


class Command(BaseCommand):
    help = 'read xlsx and dump to db'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            book = xlrd.open_workbook('test_LT.xlsx')
            read_branches(book)
            read_prirces(book)
            read_mileage(book)
        except Exception:
            raise CommandError('Something goes wrong!')
        self.stdout.write(self.style.SUCCESS('Everything is ok!'))
