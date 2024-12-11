from django.http import JsonResponse
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RateLimitMiddleware(MiddlewareMixin):
    DEFAULT_RATE_LIMIT = 10  # Number of allowed requests
    DEFAULT_TIME_PERIOD = 60  # Time period in seconds

    def process_request(self, request):
        # Ignore requests for static files or admin resources
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None

        ip = self.get_client_ip(request)
        print(f"Middleware triggered for IP: {ip}")

        rate_limit = self.DEFAULT_RATE_LIMIT
        time_period = self.DEFAULT_TIME_PERIOD

        # Check for custom rate limit from request headers
        custom_rate_limit = request.META.get('HTTP_X_RATE_LIMIT')
        if custom_rate_limit:
            try:
                rate_limit = int(custom_rate_limit)
            except ValueError:
                pass  # Fall back to default if invalid

        key = f'rate-limit-{ip}'

        # Atomically increment the request count
        request_count = cache.get(key, 0)
        if request_count == 0:
            cache.set(key, 1, timeout=time_period)
        else:
            request_count = cache.incr(key)

        print(f"Current request count for {ip}: {request_count}")

        # Check if the rate limit is exceeded
        if request_count > rate_limit:
            print(f"Rate limit exceeded for IP: {ip}")
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
