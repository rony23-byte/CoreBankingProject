from _typeshed import SupportsLenAndGetItem
from datetime import date
import decimal
from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.fields import related
from django.utils import timezone
import uuid
from decimal import ROUND_HALF_UP, Decimal


#we will create 4 classes Namely: Loans,Payment and client will inherit from base class.We will then describe the attributes of class
class Base(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    date=models.DateTimeField
    active=models.BooleanField(default=True)
    updated=models.DatetimeField(auto_now_add=True)

class Loan(Base):
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    term=models.PositiveSmallIntegerField
    rate=models.DecimalField
    client=models.ForeignKey("mayerapi.Client", verbose_name=("client_id"), on_delete=models.DO_NOTHING)
    def balance(self,date:timezone.datetime = timezone.now()):
        payments=self.payment_set.filter(payment=payment.MADE)
        payments=payments.filter(date__lte=date)
        debit=self.installment *term
        credit=sum(payments.list_values('amount',flat=True))
        return Decimal(debit-credit)
    @property#created as an instance of the object.Made when an object is called
    def installment(self):
        rate=Decimal(f'{self.rate}')
        term=Decimal(self.term)
        r=rate/term
        installment=(TO BE FILLED SOON)
        return installment.quantize(Decimal('.00',rounding=ROUND_HALF_UP))
    @classmethod#makes a method whose first argument is the class its called.

    def interest_rate(client:Base ,rate:Decimal):
         prev_loan=Loan.objects.filter(client=client.id).order_by('date')


         if not prev_loan:
            return rate

         if prev_loan.balance(None) >0:
            raise ValueError('Pending loan')

         if missed_payments>3:
              raise ValueError('MISSED TOO MANY PAYMENTS')   
         return  #we will need to reeuce the loan limit that the user can access. 
   
    def __str__(self) -> str:
        return f'{self.id}'
    

class Payment(Base):
    MADE='made'
    MISSED='missed'
    PAYMENT=((MADE,'made'),(MISSED,'missed'))
    loan=models.ForeignKey(
        to='mayerapi.Loan',on_delete=models.CASCADE
    )
    payment=models.CharField(max_length=6,choices=PAYMENT,default=MISSED)
    amount=models.DecimalField(
        max_digits= 20, decimal_places=2
    )
    def validate(self)->None:
        if self.amount!=self.loan.installment:
              raise ValueError(f'You  must pay ${self.loan.installment}')
        last_payment=(
            self.loan.payment_set.filter(date=self.date.month.week)
            .order_by('date','updated').first()

        )  

    def __str__(self):
        return str(self.id)
        #cuid represents the unique id of a client
class Client(Base):
    name=models.CharField(max_length=300,)
    surname=models.Charfield(max_length=255)
    email= models.EmailField(max_length=230)
    telephone=models.CharField(max_length=320)
    date=models.DateTimeField(auto_now_add=True,blank=True)
    cuid=models.CharField(
        max_length=14,unique=True,verbose_name=('natural persons register')
    )
class Meta:
    verbose_name='Client'
    verbose_name_plural='Clients'

    def __str__(self) ->str:
        return str(self.id)
       
