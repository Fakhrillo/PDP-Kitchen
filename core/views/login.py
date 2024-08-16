from eskiz_sms import EskizSMS
import random, re, redis
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from core.models import Student

from environs import Env
env = Env()
env.read_env()

r = redis.Redis(host='localhost', port=6379)


class SendUserVerificationCode(APIView):

    @extend_schema(
        summary="Send Verification Code",
        description=(
            "This API endpoint sends a 6-digit verification code to the user's phone number "
            "if the phone number exists in the system."
        ),
        request=inline_serializer(
            name='SendUserVerificationCodeRequest',
            fields={
                'phone': serializers.CharField()
            }
        ),
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='SendUserVerificationCodeResponseSuccess',
                fields={
                    'message': serializers.CharField()
                }
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='SendUserVerificationCodeResponseNotFound',
                fields={
                    'message': serializers.CharField()
                }
            )
        },
        examples=[
            OpenApiExample(
                name="Success Example",
                value={"message": "Verification code sent successfully"},
                response_only=True,
                status_codes=[status.HTTP_200_OK],
            ),
            OpenApiExample(
                name="User Not Found Example",
                value={"message": "User not found"},
                response_only=True,
                status_codes=[status.HTTP_404_NOT_FOUND],
            ),
        ],
    )

    def post(self, request):
        user_phone = request.data.get('phone')
        get_user = Student.objects.get(phone_number=user_phone)
        if get_user:
            ver_code = ''.join(random.choices('0123456789', k=6))
            r.set(f"verification_code:{user_phone}", ver_code, ex=60)
            send_SMS(user_phone, ver_code)
            return Response({"message": "Verification code sent successfully"}, status=200)
        else:
            return Response({"message": "User not found"}, status=404)


class VerifyUserCode(APIView):

    @extend_schema(
        summary="Verify User Code",
        description=(
            "This API endpoint verifies the code entered by the user with the one stored in the system. "
            "It checks if the provided code matches the code sent to the user's phone number."
        ),
        request=inline_serializer(
            name='VerifyUserCodeRequest',
            fields={
                'phone': serializers.CharField(),
                'verification_code': serializers.CharField()
            }
        ),
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='VerifyUserCodeResponseSuccess',
                fields={
                    'message': serializers.CharField()
                }
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='VerifyUserCodeResponseBadRequest',
                fields={
                    'message': serializers.CharField()
                }
            )
        },
        examples=[
            OpenApiExample(
                name="Success Example",
                value={"message": "Verification code is correct"},
                response_only=True,
                status_codes=[status.HTTP_200_OK],
            ),
            OpenApiExample(
                name="Incorrect Code Example",
                value={"message": "Verification code is incorrect"},
                response_only=True,
                status_codes=[status.HTTP_400_BAD_REQUEST],
            ),
        ],
    )

    def post(self, request):
        user_phone = request.data.get('phone')
        entered_code = request.data.get('verification_code')
        stored_code = r.get(f"verification_code:{user_phone}")
        if stored_code and entered_code == stored_code.decode('utf-8'):
            return Response({"message": "Verification code is correct"}, status=200)
        else:
            return Response({"message": "Verification code is incorrect"}, status=400)



def send_SMS(user_phone, random_code):
    print(f"For user {user_phone}, verification code {random_code}")
    # email = env('email')
    # password = env('password')
    # cleaned_number = re.sub(r'\+', '', user_phone)
    # eskiz = EskizSMS(email=email, password=password)
    # eskiz.send_sms(cleaned_number, f'<#> Your verification code: {random_code}', from_whom='4546', callback_url=None)
