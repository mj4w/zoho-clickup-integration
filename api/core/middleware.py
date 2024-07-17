from django.utils.deprecation import MiddlewareMixin

class TokenMiddleware(MiddlewareMixin):
    def process_request(self,request):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMzA4NjIwLCJpYXQiOjE3MjEyMjIyMjAsImp0aSI6ImNjODdjZDUyNmYxMzRkMzBiNjI3OWFlNTA3OTlhY2M3IiwidXNlcl9pZCI6MX0.AGBpakg9nq1nHEJQyQYWOxP16MmbUJODHeBKxJrFpsM" # put a token here
        if not request.META.get('HTTP_AUTHORIZATION'):
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'