from django.utils.timezone import now
from .models import RequestLog
from ipware import get_client_ip

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        path = request.path

        # Log the request
        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=now(),
                path=path
            )

        response = self.get_response(request)
        return response
