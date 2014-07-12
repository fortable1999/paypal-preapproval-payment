"""
Paypal API Interface classes
=====
Author Zhao
How to use:
    (also as doctest)

"""
import requests

from payments.exceptions import RestAPIInvokeError, RestAPIInvokeTimeout

class RestApiMixin:
    """
    Mixin for API Call Models
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

        invoke_query = self.get_invoke_query()

        try:
            resp = getattr(requests, method.lower())(
                self.get_endpoint(),
                data = self.get_invoke_request_formatter(invoke_query),
                headers = self.get_invoke_headers(),
                timeout = self.get_timeout(),
            )
        except requests.exceptions.Timeout as e:
            self.invoke_timeout()
            raise RestAPIInvokeTimeout

        if resp.status_code == 200:
            # if rest api success
            result = self.get_invoke_response_formatter(resp.text)
            self.invoke_success(result)
            self.after_invoke(resp)
            return

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
        raise 

    def after_invoke(self, invoke_resp):
        """
        docstring for after_invoke
        """
        pass

    def get_endpoint(self, resource=""):
        """
        return url for Endpoint 
        """
        endpoint = getattr(self, 'endpoint', None)
        if not endpoint:
            raise NotImplementedError('Subclasses must define this method.')
        return endpoint + resource

    def get_resource_name(self):
        return self.resource_name

    def get_invoke_headers(self):
        """
        invoke_headers
        """
        invoke_headers = getattr(self, 'invoke_headers', None)
        if not invoke_headers:
            raise NotImplementedError('Subclasses must define this method.')
        return invoke_headers 

    def get_invoke_query(self):
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


class PayPalRestAPIMixin(RestApiMixin):
    use_sandbox = True
    endpoint_name = None
    endpoint = {
        "sandbox_adaptive_payment": "https://svcs.paypal.com/AdaptiveAccounts/",
        "adaptive_payment": "https://svcs.paypal.com/AdaptiveAccounts/",
    }

    def get_endpoint(self):
        if self

