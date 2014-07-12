"""
Payment Action Type
defined:
https://developer.paypal.com/docs/classic/api/adaptive-payments/Pay_API_Operation/
"""
ACTION_TYPE_CHOICES = (

    # Use this option if you are not using the Pay request in combination 
    # with ExecutePayment
    ('PAY', 'Simple Payment'),

    # Use this option to set up the payment instructions with 
    # SetPaymentOptions and then execute the payment at a later time 
    # with the ExecutePayment.
    ('CREATE', 'Execute payment later'),

    # For chained payments only, 
    # specify this value to delay payments to the secondary receivers; 
    # only the payment to the primary receiver is processed.
    ('PAY_PRIMARY', 'Delay payment'),
)
