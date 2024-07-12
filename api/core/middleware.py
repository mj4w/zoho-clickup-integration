from django.utils.deprecation import MiddlewareMixin

class TokenMiddleware(MiddlewareMixin):
    def process_request(self,request):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwODY1NDkwLCJpYXQiOjE3MjA3NzkwOTAsImp0aSI6ImUxZWZiNWY2NTNkODQzMDg4YTQ0MDk4NWY2MDFlMDNkIiwidXNlcl9pZCI6MX0.bfqLMpnQeg2Q5fuimli38oV53vCuDYVIfwH27JhpjAM" # put a token here
        if not request.META.get('HTTP_AUTHORIZATION'):
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'