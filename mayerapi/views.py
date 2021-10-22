from datetime import timezone
from django.shortcuts import render
from django.utils import openapi
from drf_yasg.views import get_schema_view
 


from rest_framework import  permissions,response,status,viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from mayerapi import serializers
from mayerapi.models import Client,Loan, Payment
# Create your views here.
class LoanViewSets(viewsets.ModelViewSet):
    '''
    retreive:
    retrieve and return the given  loan
    list:
     return a list of all the existing loans
     create:
         Create a new loan
    

    '''
    queryset=Loans.objects.all()
    serializer_class=LoanSerializer

    @action(detail=True,methods=['post','get'])
    def payment(self,request,pk=None):
         '''
         get:
          return a list of the payments made for a given loan
          post:
          Create a new payment for a given loan

         '''
         obj=self.get_object()
         if request.method=='GET':
             return response.Response(
                PaymentSerializer(obj.payment_set.all(),many=True).data,status=status.HTTP_200_OK,
             )
         payment=request.data
         payment['loan']=pk
         serializer= PaymentSerializer(data=request.data)

         if serializer.is_valid(raise_exception=True):
             serializer.save ()
             return response.Response(serializer.data,status=status.HTTP_201_CREATED)
    @action(detail=True,methods=['get'])
    def balance(self,request,pk=None):
        '''
        get:
        Return the loan balance for a given date
        '''#none implies that we can have a
        date=request.query_params.get('date',None)
        if not date:
            date=date.timzeone.now()
        else:
            try:
                date=datetime.fromisoformat(date)
            except ValueError:
                date=dateparse.parse_datetime(date)
        
        if type(date)==datetime and not date.tzinfo:
            date=timezone.make_aware(date)
        loan=self.get_object()
        return response.Response({'balance':loan.balance(date)},status=200)

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class=ClientSerializer
    

    def get_queryset(self):
        queryset=Client.objects.all()
        cuid=self.request.query_params.get('cuid',None)
        email=self.request.query_params.get('email',None)
        telephone=self.request.query_params.get('telephone', None)


        if cuid:
            queryset=queryset.filter('cuid')

        if email:
           queryset=queryset.filter('email')
        
        if telephone:
            queryset=queryset.filter('telephone')
               
        return queryset


    def  create(self,request,*args,kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)#get the header of the serialized data.
        return Response({'client_id':serializer.data['id']},status=status.HTTP_201_CREATED,headers=headers)

schema_view=get_schema_view(
    openapi.Info(
        title='MAYERCAPITAL  API',
        default_version='1.0',
        description='A comphrehensive API  to manage payments for a fintech based company'
        contact=openapi.]Contact(
            name='Mayercapital dev' ,url=''
        ),
    public=False,
    permission_classes=(permission_classes#filled out)
    validators=['mayerCB'],
)        