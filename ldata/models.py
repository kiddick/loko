from django.core.validators import MaxValueValidator
from django.db import models


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


class Mileage(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MaxValueValidator(9999)])
    km = models.IntegerField()

    def __str__(self):
        return f'{self.branch} - {self.train} - {self.year} - {self.km}'
