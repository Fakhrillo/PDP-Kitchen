from ..models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
import face_recognition
import numpy as np

class UserCheck(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.encodings = {}

    def post(self, request, *args, **kwargs):
        try:
            student_id = request.data.get('student_id')
            uploaded_file = request.FILES.get('photo')

            if not student_id or not uploaded_file:
                return Response({'error': 'User ID and photo are required.'}, status=400)

            pil_image = Image.open(uploaded_file)
            test_image = np.array(pil_image)

            self.load_known_encodings(student_id)

            if student_id not in self.encodings:
                return Response({'error': 'User ID not found.'}, status=404)

            test_encoding = face_recognition.face_encodings(test_image)
            if not test_encoding:
                return Response({'error': 'No face detected in the uploaded image.'}, status=400)
            test_encoding = test_encoding[0]

            known_encodings, names = self.get_known_encodings_and_names()

            distances = np.linalg.norm(known_encodings - test_encoding, axis=1)
            min_distance_index = np.argmin(distances)
            min_distance = distances[min_distance_index]

            threshold = 0.6
            status = None
            if min_distance < threshold:
                name = names[min_distance_index]
                status = "Successfully"
                identified_user_id = [key for key, value in self.encodings.items() if value[0] == name][0]
            else:
                name = 'unknown'
                status = "Failed"
                identified_user_id = -1

            return Response({
                'match': status,
                'name': name,
                })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def load_known_encodings(self, student_id):
        try:
            user = Student.objects.get(student_id=student_id)
            
            known_image = face_recognition.load_image_file(user.photo.path)
            encoding = face_recognition.face_encodings(known_image)
            
            if encoding:  # Ensure that an encoding is found
                self.encodings[user.student_id] = [user.first_name, encoding[0]]
        except Student.DoesNotExist:
            print(f'User with ID {student_id} does not exist.')
        except Exception as e:
            print(f'Failed to load known encodings: {e}')

    def get_known_encodings_and_names(self):
        known_encodings = []
        names = []
        for student_id, (name, encoding) in self.encodings.items():
            known_encodings.append(encoding)
            names.append(name)
        return np.array(known_encodings), names
