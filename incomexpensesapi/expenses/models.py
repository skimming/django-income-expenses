from django.db import models

from authentication.models import User

# Create your models here.

class Expense(models.Model):

    # definition of enums
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES','ONLINE_SERVICES'),
        ('TRAVEL','TRAVEL'),
        ('FOOD','FOOD'),
        ('RENT','RENT'),
        ('OTHERS','OTHERS'),
    ]
    # use the enum above
    category=models.CharField(choices=CATEGORY_OPTIONS, max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    # to refers to the model
    # CASCADE option has automatic deletion of expenses 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"Expense: id[{self.id}], description[{self.description}]; amount[{self.amount}]"