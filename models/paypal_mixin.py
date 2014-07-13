"""
Paypal API Interface classes
=====
Author Zhao
How to use:
    (also as doctest)

"""
from django.conf import settings
from django.contrib.sites.models import Site
import datetime
import json
import requests
import pytz

from payment.exceptions import RestAPIInvokeError, RestAPIInvokeTimeout

class RestApiMixin:
    """
    Mixin for API Call Models
    You need to overload:

    """
    timeout = 3
    resource_name = ""

    def before_invoke(self):
        """
        docstring for before_invoke
        """
        pass

    def invoke(self, method, **kwargs):
        """
        docstring for invoke
        """
        self.before_invoke()

        invoke_query = self.get_invoke_query(**kwargs)

        print(self.get_endpoint(**kwargs))
        print(self.get_invoke_headers())
        print(self.get_invoke_request_formatter()(invoke_query))
        try:
            resp = getattr(requests, method.lower())(
                self.get_endpoint(**kwargs),
                data = self.get_invoke_request_formatter()(invoke_query),
                headers = self.get_invoke_headers(),
                timeout = self.get_timeout(),
            )
        except requests.exceptions.Timeout as e:
            self.invoke_timeout()
            raise RestAPIInvokeTimeout

        if resp.status_code == 200:
            # if rest api success
            print(resp.status_code, resp.text)
            result = self.get_invoke_response_formatter()(resp.text)
            self.invoke_response_valid(result)
            self.invoke_success(result)
            self.after_invoke(result)
            return result

        # if rest api failed
        result = self.get_invoke_exception_formatter(resp.text, resp.status_code)
        self.invoke_failure(resp)
        raise RestAPIInvokeError(resp.text)

    def invoke_success(self, invoke_resp):
        """
        docstring for invoke_success
        """
        raise NotImplementedError('Subclasses must define this method.')

    def invoke_failure(self, resp):
        """
        docstring for invoke_failure
        """
        raise NotImplementedError('Subclasses must define this method.')

    def invoke_timeout(self):
        """
        docstring for invoke_success
        """
        raise NotImplementedError('Subclasses must define this method.')

    def invoke_response_valid(self, invoke_result):
        if invoke_result['responseEnvelope']['ack'].lower() != 'success':
            raise RestAPIInvokeError(invoke_result['error'])

    def after_invoke(self, invoke_result):
        """
        docstring for after_invoke
        """
        print("*** AFTER INVOKE ***")

    def get_endpoint(self, **kwargs):
        """
        return url for Endpoint 
        """
        endpoint = getattr(self, 'endpoint', None)
        if not endpoint:
            raise NotImplementedError('Subclasses must define this method.')
        return endpoint

    def get_invoke_headers(self):
        """
        invoke_headers
        """
        invoke_headers = getattr(self, 'invoke_headers', None)
        if not invoke_headers:
            raise NotImplementedError('Subclasses must define this method.')
        return invoke_headers 

    def get_invoke_query(self, **kwargs):
        """
        invoke_query
        """
        invoke_query = getattr(self, 'invoke_query', None)
        if not invoke_query:
            raise NotImplementedError('Subclasses must define this method.')
        return invoke_query 

    def get_invoke_request_formatter(self):
        """docstring for getinvoke_response_formatter"""
        return lambda x: x

    def get_invoke_response_formatter(self):
        """docstring for getinvoke_response_formatter"""
        return lambda x: x

    def get_invoke_exception_formatter(self, status_code=400):
        """docstring for getinvoke_response_formatter"""
        return lambda x: x

    def get_timeout(self):
        """docstring for get_timeout"""
        return self.timeout


class JsonAPIMixin:
    """
    Request and Response is json.
    """
    def get_invoke_request_json_formatter(self):
        """docstring for getinvoke_response_formatter"""
        return json.dumps 

    def get_invoke_response_json_formatter(self):
        """docstring for getinvoke_response_formatter"""
        return json.loads 

    def get_invoke_exception_json_formatter(self, status_code=400):
        """docstring for getinvoke_response_formatter"""
        return json.loads
        

class PayPalPreapprovalAPIMixin:
    """docstring for PayPalPreapprovalAPIMixin"""

    def invoke_preapproval(self, **kwargs):
        """docstring for """
        return self.invoke('post', **kwargs)

    def invoke_preapproval_details(self, **kwargs):
        """docstring for """
        return self.invoke('post', **kwargs)

    def invoke_preapproval_success(self, resp):
        """docstring for invoke"""
        print(resp)

    def get_starting_date(self, **kwargs):
        """
        TODO: use other timezone
        docstring for get_ending_date
        """
        start_date = getattr(self, 'start_date')
        return self.datetime_to_utc_str(start_date)

    def get_ending_date(self, **kwargs):
        """
        TODO: use other timezone
        docstring for get_ending_date
        """
        print(dir(self))
        end_date = getattr(self, 'end_date')
        # end_date = datetime.datetime.now() + datetime.timedelta(seconds=120)
        return self.datetime_to_utc_str(end_date)

    def get_max_amount_of_all_payments(self, **kwargs):
        """docstring for get_max_amount_of_all_payments"""
        return 35.00

    def get_invoke_preapproval_query(self, **kwargs):
        """
        docstring for api payload
        """
        return {
            "maxAmountPerPayment": self.get_max_amount_of_all_payments(**kwargs),
            "maxNumberOfPayments": self.get_max_number_of_payments(**kwargs),
            "endingDate": self.get_ending_date(**kwargs),
            "startingDate": self.get_starting_date(**kwargs),
            "maxTotalAmountOfAllPayments": self.get_max_amount_of_all_payments(**kwargs),
            "currencyCode": self.get_currency_code(**kwargs),
            "returnUrl": self.get_return_url(),
            "cancelUrl": self.get_cancel_url(),
            "requestEnvelope": self.get_request_envelope(),
        }

    def get_invoke_preapproval_details_query(self, **kwargs):
        """
        docstring for api payload
        """
        return {
            "preapprovalKey": self.get_preapproval_key(**kwargs),
            "requestEnvelope": self.get_request_envelope(),
        }

    def get_max_amount_per_payment(self, kwargs):
        """docstring for get_max_amount_per_payment"""
        if not kwargs.get('max_amount_per_payment', None):
            return kwargs['max_amount_per_payment']
        raise RestAPIInvokeError("maxAmountPerPayment not given")

    def get_max_number_of_payments(self, kwargs):
        """docstring for get_max_amount_per_payment"""
        if not kwargs.get('max_number_of_payments', None):
            return kwargs['max_number_of_payments']
        else:
            return 1

    def get_preapproval_key(self, **kwargs):
        preapproval_key = kwargs.get('preapproval_key', None)
        if preapproval_key: return preapproval_key
        preapproval_key = getattr(self, 'preapproval_key', None)
        if preapproval_key: return preapproval_key
        raise RestAPIInvokeError("preapprovalKey not given")

    def datetime_to_utc_str(self, dt):
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        tokyo_dt = tokyo_tz.localize(dt)
        fmt = "%Y-%m-%dT%H:%M:%S"
        # utc = pytz.utc
        return tokyo_dt.astimezone(pytz.UTC).strftime(fmt)


class PayPalRestAPIMixin(RestApiMixin, JsonAPIMixin, PayPalPreapprovalAPIMixin):
    """
    Methods supported:
    Pay, PaymentDetails, Preapproval, PreapprovalDetails, CancelPreapproval
    """

    use_sandbox = True
    endpoint_name = None
    endpoint = {
        "sandbox_adaptive_payment": "https://svcs.sandbox.paypal.com/AdaptivePayments/",
        "adaptive_payment": "https://svcs.paypal.com/AdaptivePayments/",
    }

    def invoke_success(self, resp):
        pass

    def get_endpoint(self, **kwargs):
        endpoint = None
        endpoint_root = None
        if self.use_sandbox:
            print("#### USING SANDBOX ###")
            endpoint_root = self.endpoint['sandbox_adaptive_payment']
        else:
            endpoint_root = self.endpoint['adaptive_payment']
        return endpoint_root + kwargs.get('operation', "")

    def get_invoke_headers(self):
        """
        docstring for get_headers
        """
        headers = {
                "X-PAYPAL-SECURITY-USERID": settings.PAYPAL_USERID,
                "X-PAYPAL-SECURITY-PASSWORD": settings.PAYPAL_PASSWORD,
                "X-PAYPAL-SECURITY-SIGNATURE": settings.PAYPAL_SIGNATURE,
                "X-PAYPAL-APPLICATION-ID": settings.PAYPAL_APPLICATION_ID,
                "X-PAYPAL-REQUEST-DATA-FORMAT": 'JSON',
                "X-PAYPAL-RESPONSE-DATA-FORMAT": 'JSON',
        }

        return headers

    def get_invoke_query(self, **kwargs):
        """
        docstring for api payload
        """
        operation = kwargs.get('operation', None)
        if operation.lower() == "preapproval":
            return self.get_invoke_preapproval_query(**kwargs)
        if operation.lower() == "preapprovaldetails":
            return self.get_invoke_preapproval_details_query(**kwargs)
        # return {
        #     "actionType": "PAY",
        #     "currencyCode": self.get_currency_code(),
        #     "receiverList": {
        #         "receiver": self.get_receiver_list()
        #     },
        #     "returnUrl": self.get_return_url(),
        #     "cancelUrl": self.get_cancel_url(),
        #     "requestEnvelope": self.get_request_envelope(),
        # }

    def get_receiver_list(self, **kwargs):
        """
        You must overwirte this method
        """
        return  [
            {
                "amount":"1.00",
                "email":"testauthor@author.mangaconnect.com",
                "primary": "true",
            },
            {
                "amount":"1.00",
                "email":"payment@mangaconnect.com",
            },
        ]

    def get_currency_code(self, **kwargs):
        return "USD"

    def get_return_url(self, **kwargs):
        """
        You must overwirte this method
        """
        return str(Site.objects.get_current())

    def get_cancel_url(self, **kwargs):
        """docstring for get_return_url"""
        return str(Site.objects.get_current())

    def get_request_envelope(self, **kwargs):
        return {
            "errorLanguage":"en_US", 
            "detailLevel":"ReturnAll"
        }

    def get_invoke_request_formatter(self):
        """docstring for getinvoke_response_formatter"""
        return self.get_invoke_request_json_formatter()

    def get_invoke_response_formatter(self):
        """docstring for getinvoke_response_formatter"""
        return self.get_invoke_response_json_formatter()

