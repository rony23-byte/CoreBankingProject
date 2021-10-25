# CoreBankingProject
Client and Loan Management System

#features
- Loan management
- Payments control
- Outstanding balance
Tracking clients payments





## Objective

The main objective of this project is to create an API to manage clients and the loan payments control system.

## Purpose

We are trying to ensure financial inclusion by supporting SMES ensuring that they have access to credit to scale their businesses. 

## Problem
	
A fin-tech needs to create and manage the clients and keep track of the amount of money loaned and the missed/made payments. It also needs a place to retrieve the volume of outstanding debt at some point in time.We need to leverage on ai for credit scoring

## Business Rules

- If a client contracted a loan in the past and paid all without missing any payment, then his limit can be increased.
- If a client contracted a loan in the past and has been delaying payment,then then reduce the loan limit that customer can access.
- If a client contracted a loan in the past and paid all but missed more than 3 weekly payments or didn’t pay all the loan, you need to deny the new one.
The interest rate for the loan  should be placed at 20% 
 A loan processing fee of 1%

## Limitations

Loans are paid back in weekly instalments.

## Endpoints

### POST /clients

#### Summary

Create a client in the system.

#### Payload

- **name**: the client name.
- **surname**: the client surname.
- **email**: the client email.
- **telephone**: the client telephone.
- **cpf**: the client identification.

#### Example of sent data

```json
{
    "name": "Felicity",
    "surname": "Jones",
    "email": "felicity@gmail.com",
    "telephone": "11984345678",
    "loanid": "34598712387"
}
```

#### Reply

- **client_id**: unique id of a client. 

#### Example of received data

```json
{
    "client_id": 1
}
```

### POST /loans

#### Summary

Create a loan application. Loans are automatically accepted.

#### Payload

- **client_id**: the client's identification that contracted a loan.
- **amount**: loan amount in dollars.
- **term**: number of months that will take until the loan gets paid-off.
- **rate**: interest rate as decimal.
- **date**: when the loan was requested (origination date as an ISO 8601 string). 

#### Example of sent data

```json
{
    "client_id": 1,
    "amount": 1000,
    "term": 12,
    "rate": 0.05,
    "date": "2019-05-09 03:18Z"
}
```

#### Reply

- **loan_id**: unique id of the loan.
- **instalment**: monthly loan payment.

#### Example of received data

```json
{
    "loan_id": "000-0000-0000-0000",
    "instalment": 85.60
}
```

#### Notes

**Loan payment formula**

```
r = rate / term
instalment = [r + r / ((1 + r) ^ term )] x amount
```

 
``` 

### POST /loans/<:id>/payments

#### Summary

Create a record of a payment made or missed.

#### Payload

- **payment**: type of payment: made or missed.
- **date**: payment date.
- **amount**: amount of the payment made or missed in dollars.

#### Example of sent data (Payment made)

```json
{
    "payment": "made",
    "date": "2019-05-07 04:18Z",
    "amount": 85.60
}
```

#### Example of sent data (Payment missed)

```json
{
    "payment": "missed",
    "date":  "2019-05-07 04:18Z",
    "amount": 85.60
}
```

### POST /loans/<:id>/balance

#### Summary

Get the volume of outstanding debt (i.e., debt yet to be paid) at some point in time.

#### Payload

- date: loan balance until this date.

#### Example of sent data

```json
{
    "date": "2017-09-05 02:18Z"
}
```

#### Reply

- balance: outstanding debt of loan.

#### Example

```json
{
    "balance": 40
}
```


