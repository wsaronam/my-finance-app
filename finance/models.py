from django.db import models

# Create your models here.
class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('test1', 'Test1'),
        ('test2', 'Test2'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return "model test"