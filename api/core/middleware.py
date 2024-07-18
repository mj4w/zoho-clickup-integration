from django.utils.deprecation import MiddlewareMixin

class TokenMiddleware(MiddlewareMixin):
    def process_request(self,request):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMzk1MTIyLCJpYXQiOjE3MjEzMDg3MjIsImp0aSI6IjNkODZkYTA1OTU1YTRkZjdhM2I2ODkyY2M0NzYxZTQ1IiwidXNlcl9pZCI6MX0.ryqa-QT60jnW7ZnztBRfK93K-Sa31ymxpvV2yH1-e8I" # put a token here
        if not request.META.get('HTTP_AUTHORIZATION'):
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'