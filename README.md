# Django Paypal Preapproval chained payment 

### How it works:
```
for
Preapproval:
Create, Update, Read, Delete
to PayPal:
invoke_preapproval
invoke_preapproval_detail

Payment:
Create, Update, Read, Delete


# Create a pre-approval
>>> preapproval = Preapproval.objects.create()


# Create a payment in database
>>> payment = Payment.objects.create()

# Create a payment on PayPal
>>> payment.create()

# Redirect sender to login paypal
>>>


```
