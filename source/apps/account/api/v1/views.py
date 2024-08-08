from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.contrib.auth import authenticate
from .serializers import MobileNumberSerializer, VerifyCodeSerializer, CompleteRegistrationSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from apps.account.request_limiter import RequestLimiter
from apps.account.task import send_verification_code
from apps.account.utils import generate_digit_code
User = get_user_model()


class SendCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MobileNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']

        ip_address = request.META.get('REMOTE_ADDR')

        # Throttle check
        RequestLimiter.attempt(
            request, request_type="register", mobile_number=mobile_number)
        if cache.get(f'ip_blocked_{ip_address}') or cache.get(f'mobile_number_blocked_{mobile_number}'):
            return Response({"detail": "Too many attempts, try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if User.objects.filter(mobile_number=mobile_number).exists():
            return Response({"detail": "User already registered, proceed to login."}, status=status.HTTP_200_OK)
        else:
            code = generate_digit_code()
            send_verification_code(mobile_number, code)
            return Response({"detail": "Registration code sent."}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        code = serializer.validated_data['code']
        ip_address = request.META.get('REMOTE_ADDR')

        if cache.get(f'ip_blocked_{ip_address}') or cache.get(f'mobile_number_blocked_{mobile_number}'):
            return Response({"detail": "Too many attempts, try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if cache.get(f'registration_code_{mobile_number}') == int(code):
            cache.delete(f'registration_code_{mobile_number}')
            # Verification valid for 5 minutes
            cache.set(f'registration_verified_{mobile_number}', True, 300)
            return Response({"detail": "Registration verification successful."}, status=status.HTTP_200_OK)
        else:
            RequestLimiter.attempt(
                request, request_type="register", mobile_number=mobile_number)
            return Response({"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)


class CompleteRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CompleteRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']

        if cache.get(f'registration_verified_{mobile_number}'):
            user = serializer.save()
            cache.delete(f'registration_verified_{mobile_number}')
            return Response({"detail": "Registration complete."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Mobile number not verified."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.validated_data['mobile_number']
        password = serializer.validated_data['password']

        ip_address = request.META.get('REMOTE_ADDR')

        # Throttle check
        if cache.get(f'ip_blocked_{ip_address}') or cache.get(f'mobile_number_blocked_{mobile_number}'):
            return Response({"detail": "Too many attempts, try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        user = authenticate(username=mobile_number, password=password)
        if user:
            # Here you can return a token or any other authentication method you use
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        else:
            RequestLimiter.attempt(
                request, request_type="login", mobile_number=mobile_number)
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
