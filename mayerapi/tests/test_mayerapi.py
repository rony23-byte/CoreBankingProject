from _typeshed import Self
from datetime import timedelta
from decimal import Decimal
from urllib import parse
from django.test import TestCase
from django.utils import timezone
from rest_framework.test  import APIClient
from mayerapi.tests.utils import create_client


class TestLoan(TestCase):
    def setUp(self)->None:
        self.api=APIClient()
        self.loan_id=None
        self.payment_id=None
    def new_loan(self)->int:
        if self.loan_id:
            return 201
        client_id=create_client().data.get("client_id")
        post={
               "amount":1000,
               'term':12,
                "rate":0.21,
               "date":timezone.now(),
             "client_id":client_id,

           }

        resp=self.api.post("mayerapi/loans/",post,format="json")

        if resp.status_code==201:
            self.loan_id=resp.data.get('loan_id',None)
        
        return resp.status_code
         
    def new_payment(self)->int:
        self.new_loan()

        if self.payment_id  :
            return 201
        post={"payment":"made","date":timezone.now(),"amount":}
        resp=self.api.post(
        f"/api/loans/{self.loan_id}/payments/",post, format="json"
        )      
       
        if resp.status_code==201:
            self.payment_id=resp.data.get("amount",None)
        return resp.status_code



    def  test_new_loan(self)->None:
        status=self.new_loan()
        self.assertEqual(status,201)
    def test_loan_field(self)->None:
        self.new_loan()
        resp=self.api.get(f'/mayerapi/loans/{self.laon_id}/',format="json")
        self.assertEqual(resp.status_code,200)
        self.assertEqual({"loan_id","installment"},set(resp.data.keys()))

    def test_new_payment(self)->None:
        status=self.new_payment()
        self.assertEqual(status,201)
    
    def test_loan_balance(self)->None:
        self.new_payment()
        date=parse.quote_plus(str(timezone.now()))
        resp=self.api.get(f"/mayerapi/loans{self.loan_id}/balance/?date={date}", format="json")
        self.assertEqual(resp.status_code,200)
    def test_loan_balance_value(self)->None:
        self.new_payment()
        date=parse.quote_plus(str(timezone.now()))
        resp=self.api.get(f"/mayerapi/loans{self.loan_id}/balance/?date={date}", format="json")
        balance=resp.data.get('balance')
        self.assertEqual(balance,Decimal('9867.54'))
    def test_loan_balance_incorrect_value(self)->None:
        self.new_payment()
        date=parse.quote_plus(str(timezone.now()))
        resp=self.api.get(f"/mayerapi/loans{self.loan_id}/balance/?date={date}", format="json")
        balance=resp.data.get('balance')
        self.assertEqual(balance, Decimal("1027.32"))


class TestClient(TestCase):
    def test_post_client(self)->None:
        res=create_client
        self.assertEqual(201,res.status_code)
        self.assertEqual({"client_id"},res.data.keys())
       




