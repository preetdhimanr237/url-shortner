from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShortURLSerializer
from .models import ShortURL
import uuid

# Create your views here.
class ShortURLView(APIView):

    # def get(self,request):
    #     urls = ShortURL.objects.all()
    #     serializer = ShortURLSerializer(urls, many = True)
    #     return Response(serializer.data)
    def get(self, request):
        urls = ShortURL.objects.all().values()
        return Response(list(urls))
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


def redirect_url(request,code):
    url = get_object_or_404(ShortURL,short_code=code)
    url.clicks+=1
    url.save(update_fields=["clicks"])
    return redirect(url.original_url)
    
