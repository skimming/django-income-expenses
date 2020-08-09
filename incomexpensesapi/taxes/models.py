from django.db import models

from authentication.models import User

# Create your models here.

class Tax(models.Model):

    # definition of enums
    TAXTYPE_OPTIONS = [
        ('SALES','SALES'),
        ('PAYROLL','PAYROLL'),
        ('SOCIALSECURITY','SOCIALSECURITY'),
    ]

    PAYEE_OPTIONS = [
        ('FEDERAL', 'FEDERAL'),
        ('STATE', 'STATE'),
        ('LOCAL', 'LOCAL'),
    ]
    # use the enum above
    taxtype = models.CharField(choices=TAXTYPE_OPTIONS, max_length=30, default="SALES")
    payee = models.CharField(choices=PAYEE_OPTIONS, max_length=30, default="FEDERAL")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    # to refers to the model
    # CASCADE option has automatic deletion of expenses 
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering: ['-date']     # identifies how the results should be ordered


    def __str__(self):
        return f"Tax: [{self.owner}'s] id[{self.id}],  description[{self.description}]; amount[{self.amount}]"