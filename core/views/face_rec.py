from ..models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.utils import inline_serializer
from PIL import Image
import face_recognition
import numpy as np

class UserCheck(APIView):

    @extend_schema(
        summary="User Identity Verification",
        description=(
            "This API endpoint verifies the identity of a user based on the provided student ID "
            "and a photo. It compares the face in the uploaded photo with the known encoding of "
            "the student associated with the provided ID."
        ),
        request=inline_serializer(
            name='UserCheckRequest',
            fields={
                'student_id': serializers.CharField(),
                'photo': serializers.ImageField()
            }
        ),
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='UserCheckResponseSuccess',
                fields={
                    'match': serializers.CharField(),
                    'name': serializers.CharField()
                }
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='UserCheckResponseBadRequest',
                fields={
                    'error': serializers.CharField()
                }
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='UserCheckResponseNotFound',
                fields={
                    'error': serializers.CharField()
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: inline_serializer(
                name='UserCheckResponseServerError',
                fields={
                    'error': serializers.CharField()
                }
            ),
        },
        examples=[
            OpenApiExample(
                name="Success Example",
                value={"match": "Successfully", "name": "John Doe"},
                response_only=True,
                status_codes=[status.HTTP_200_OK],
            ),
            OpenApiExample(
                name="Failure Example",
                value={"match": "Failed", "name": "unknown"},
                response_only=True,
                status_codes=[status.HTTP_200_OK],
            ),
            OpenApiExample(
                name="Bad Request Example",
                value={"error": "User ID and photo are required."},
                response_only=True,
                status_codes=[status.HTTP_400_BAD_REQUEST],
            ),
            OpenApiExample(
                name="User Not Found Example",
                value={"error": "User ID not found."},
                response_only=True,
                status_codes=[status.HTTP_404_NOT_FOUND],
            ),
            OpenApiExample(
                name="Server Error Example",
                value={"error": "Some unexpected error occurred."},
                response_only=True,
                status_codes=[status.HTTP_500_INTERNAL_SERVER_ERROR],
            ),
        ],
    )

    def post(self, request, *args, **kwargs):
        try:
            # Assume the image is sent as form data named 'photo'
            student_id = int(request.data['student_id'])
            uploaded_file = request.FILES['photo']
            pil_image = Image.open(uploaded_file)
            test_image = np.array(pil_image)

            test_encoding = face_recognition.face_encodings(test_image)[0]

            # Get the known user information
            user_info = Student.objects.get(student_id=student_id)
            known_image = np.array(face_recognition.load_image_file(user_info.photo.path))
            known_encodings = face_recognition.face_encodings(known_image)[0]

            # Calculate distance between the uploaded encoding and the known encoding
            distance = np.linalg.norm(known_encodings - test_encoding)

            # Set threshold to determine match
            if distance < 0.40:
                name = user_info.first_name
            else:
                name = 'unknown'

            return Response({'name': name})
        except Exception as e:
            return Response({'error': str(e)}, status=400)