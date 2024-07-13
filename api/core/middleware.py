from django.utils.deprecation import MiddlewareMixin

class TokenMiddleware(MiddlewareMixin):
    def process_request(self,request):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTU2NjI5LCJpYXQiOjE3MjA4NzAyMjksImp0aSI6IjFhZmM2Y2M0YmU0ODRkOTdhNTRmZTQyYmE4MTNmOGM2IiwidXNlcl9pZCI6MX0.LIv2pz-VCP4vKxeV22eSAxjzrAzblJq7zWoBTj_U44Y" # put a token here
        if not request.META.get('HTTP_AUTHORIZATION'):
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'