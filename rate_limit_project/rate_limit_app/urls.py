from django.urls import path
from .views import RateLimitedView

urlpatterns = [
    path('rate-limit/', RateLimitedView.as_view(), name='rate_limit'),
]