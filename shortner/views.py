from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShortURLSerializer
import uuid

# Create your views here.
class ShortURLView(APIView):

    def get(self,request):
        return Response({"message":"Welcome to URL Shortner!"})

    def post(self, request):
        data = request.data.copy()
        data["short_code"] = uuid.uuid4().hex[:6]

        serializer = ShortURLSerializer(data=data)

        if serializer.is_valid():
            saved_url = serializer.save()

            print("SAVED SUCCESSFULLY:", saved_url.id)

            return Response(serializer.data, status=201)

        print("ERROR:", serializer.errors)
        return Response(serializer.errors, status=400)


