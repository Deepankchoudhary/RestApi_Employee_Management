import jwt
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework_jwt.serializers import jwt_payload_handler

from .serializers import RegisterSerializer
from rest_framework.views import APIView
from .models import Employee
from rest_framework.response import Response
from .serializers import EmplyeeSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "user": serializer.data,
            "message": "User Created Successfully..!",
        })


class Login_Auth(APIView):

    @permission_classes([AllowAny, ])
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    data = request.data
                    name = data.get("username")

                    return Response({"username": name, "Message": "Login successfully..!!", "Token": token},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)


class AddEmployee(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data['added_by'] = request.user.id
        serializer = EmplyeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Emplyee": serializer.data,
                "message": "Emplyee Added Successfully..!",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Employeelist(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        emplyee = Employee.objects.all()
        serializer = EmplyeeSerializer(emplyee, many=True)
        return Response({"Message": "List of Emplyee..!", "Emplyee": serializer.data})


class Delete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        data = request.data
        id = data.get("id")
        id2 = data['id']
        try:
            Employee.objects.get(id=id).delete()
            return Response({'message': 'The Emplyee is deleted successfully..!'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'The Emplyee does not exist'}, status=status.HTTP_404_NOT_FOUND)


class Update(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        data = request.data
        id = data.get("id")
        emplyee = Employee.objects.get(id=id)
        serializer = EmplyeeSerializer(emplyee, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return JsonResponse({'message': 'Emplyee was updated successfully!'}, status=status.HTTP_200_ok)
        except:
            return Response({'message': 'The Emplyee does not exist'}, status=status.HTTP_404_NOT_FOUND)


