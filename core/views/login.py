from eskiz_sms import EskizSMS
import random, re, redis
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Student

from environs import Env
env = Env()
env.read_env()

r = redis.Redis(host='localhost', port=6379)


class SendUserVerificationCode(APIView):
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
