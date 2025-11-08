from django.utils.timezone import now
from .models import RequestLog
from ipware import get_client_ip

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        # Block blacklisted IPs
        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied.")

        # Log request
        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=now(),
                path=request.path
            )

        return self.get_response(request)
