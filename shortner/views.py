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
        existing_url = ShortURL.objects.filter(original_url=data.get("original_url")).first()
        if existing_url:
            serializer= ShortURLSerializer(existing_url)
            return Response(serializer.data,status=200)
        if not data.get("short_code"):
            data["short_code"] = uuid.uuid4().hex[:6]

        if ShortURL.objects.filter(short_code=data["short_code"]).exists():
            return Response("error: this code is already taken",status=400)
        serializer = ShortURLSerializer(data=data)

        if serializer.is_valid():
            saved_url = serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
            


        


def redirect_url(request,code):
    url = get_object_or_404(ShortURL,short_code=code)
    url.clicks+=1
    url.save(update_fields=["clicks"])
    return redirect(url.original_url)
    

class ShortURLDetailView(APIView):
    def delete(self,request,pk):
        url = get_object_or_404(ShortURL,id=pk)
        url.delete()
        return Response({"Message":"Url deleted successfully"},status=200)


    def put(self, request, pk):
        url = get_object_or_404(ShortURL, id=pk)

        serializer = ShortURLSerializer(
            url,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)    

        return Response(serializer.errors, status=400)