# from rest_framework.throttling import UserRateThrottle
# from rest_framework.views import APIView
# from rest_framework.response import Response

# class RateLimitedView(APIView):
#     throttle_classes = [UserRateThrottle]

#     def get(self, request):
#         return Response({"message": "Hello, world!"})


from rest_framework.views import APIView
from rest_framework.response import Response

class RateLimitedView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
