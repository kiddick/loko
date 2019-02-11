import operator
from collections import defaultdict
from functools import reduce

from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q, FloatField
from django.db.models import F
from django.db.models import Sum


class Train(models.Model):
    name = models.CharField(max_length=256)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.price}'


class Branch(models.Model):
    name = models.CharField(max_length=256)
    trains = models.ManyToManyField(Train)

    def __str__(self):
        return self.name


class MileageQuerySet(models.QuerySet):
    def get_stats(self, query, year_from, year_to):
        branches = []
        branches_trains = defaultdict(list)
        for item in query.split(','):
            if '_' in item:
                b, t = item.split('_')
                branches_trains[b].append(t)
            else:
                branches.append(item)
        branches = [Q(branch=i) for i in branches]
        branches_trains = [(Q(branch=b) & Q(train__in=t)) for b,t in branches_trains.items()]
        period = Q(year__range=[year_from, year_to])
        # qquery = self.annotate(price=select_related('train'))
        qquery = self.select_related('train')
        qquery =  qquery.filter(reduce(operator.or_, (*branches, *branches_trains)) & period)
        # qquery =  self.filter(reduce(operator.or_, (*branches, *branches_trains)) & period)
        # qquery =  qquery.aggregate(total=Sum(F('km')*F('train__price'), output_field=FloatField()))
        # for i in qquery.all():
        #     print(i)
        qquery = qquery.values('year').annotate(total=Sum(F('km')*F('train__price'), output_field=FloatField()))
        print(qquery.query)
        return qquery


class Mileage(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MaxValueValidator(9999)])
    km = models.FloatField()
    objects = MileageQuerySet.as_manager()

    def __str__(self):
        return f'{self.branch} - {self.train} - {self.year} - {self.km}'
