from  django.test import TestCase
from mayerapi.models import Payment,Loan,Client
from django.db.utils import IntegrityError
from datetime import datetime
from decimal import  Decimal
import os.path

from mayerapi.tests.utils import(
    create_client_from_model,
    create_loan_from_model,
    create_payment_from_model

)

class TestPaymentModel(TestCase):
    def setUp(self) -> None:
        client=create_client_from_model
        loan=create_loan_from_model
        Payment=create_payment_from_model

    def test_payment_instance(self):
        expected_payment="made"
        expected_date='2022-01-03'
        expected_amount=400
        

        self.assertIsInstance(self.payment,Payment)
        self.assertIsInstance(self.payment.loan,Loan)
        self.assertEqual(expected_amount=self.payment.amount)
        self.assertEqual(expected_loan=self.payment.loan)
        self.assertEqual(expected_date=self.payment.date)

    def test_validate_raises_exception(self):
        with self.assertRaises(ValueError):
            self.payment.validate()

    def test_payment__str__(self):
        self.assertEqual(str(self.payment),str(self.payment.id))


class TestLoanModel(TestCase):
    def setUp(self) -> None:
        self.client=create_client_from_model
        self.loan=create_loan_from_model

    def test_loan_instance(self):
        expected_amount=3000
        expected_term=1
        expected_rate=0.21
        expected_date = "2022-06-12"
        self.assertIsInstance(self.loan,Loan)
        self.assertIsInstance(self.loan,Client)
        self.assertEqual(expected_amount,self.loan.amount)
        self.assertEqual(expected_term,self.loan.term)
        self.assertEqual(expected_rate,self.loan.rate)
        
    def test_loan__str__(self)->None:
        self.assertEqual(str(self.loan),str(self.loan.id))
    def test_installment(self)->None:
        for loan in Loan:
            with self.subTest(
                name=f' rate:{loan.rate},amount:{loan.amount}, term:{loan.term}'
            ):
               rate = Decimal(loan.rate)
               term = Decimal(loan.term)
               amount = Decimal(loan.amount.replace(",", ""))
               expected_installment = Decimal(loan.installment.replace(",", ""))
               actual_loan = create_loan_from_model(
                    self.client, rate=rate, term=term, amount=amount
               )
            self.assertEqual(expected_installment,actual_loan)
    def  test_interest_rate(self):
        with self.assertRaises(ValueError):
             Loan.interest_rate(self.loan.client,0.21)          
            
class TestClientModel(TestCase):
    def setUp(self)->None:
        self.client=create_client_from_model
    def test_client_instance(self) ->None:
        expected_name='Nicholas'
        expected_surnname='Wabera'
        expected_email='nicholaswabera@gmail.com'
        expected_telephone="+254712165970"
        expected_cuid= 'MDQ2134XYWE'
        self.assertIsInstance(self.client,Client)
        self.assertIsInstance(self.client.date,datetime)
        self.assertEqual(expected_name,self.client.name)
        self.assertEqual(expected_surnname,self.client.surnname)
        self.assertEqual(expected_email,self.client.email)
        self.assertEqual(expected_telephone,self.client.telephone)
        self.assertEqual(expected_cuid,self.client.cuid)
        
    def test_client_instance_blank_telephone(self):
         client=create_client_from_model()
         self.assertEqual(Client.telephone)
    def test_client_instance_unique_cuid(self):
        with self.assertRaises(IntegrityError):

    def test_client__str__(self):
        self.assertEqual(str(self.client),str(self.client.id))




        



    


