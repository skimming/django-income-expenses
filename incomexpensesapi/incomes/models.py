from django.db import models

from authentication.models import User

# Create your models here.

class Income(models.Model):

    # definition of enums
    SOURCE_OPTIONS = [
        ('CONSULTING','CONSULTING'),
        ('REBATES','REBATES'),
        ('PURCHASE','PURCHASE'),
        ('DONATION', 'DONATION'),
        ('SALARY', 'SALARY'),
    ]
    # use the enum above
    source=models.CharField(choices=SOURCE_OPTIONS, max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    # to refers to the model
    # CASCADE option has automatic deletion of expenses 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering: ['-date']     # identifies how the results should be ordered


    def __str__(self):
        return f"Income: [{self.owner}'s] id[{self.id}],  description[{self.description}]; amount[{self.amount}]"