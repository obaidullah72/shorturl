# shortener/views.py

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShortURL
from .serializers import ShortURLSerializer
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'index.html')

def stats(request):
    return render(request, 'stats.html')

class ShortURLListCreate(APIView):
    def get(self, request):
        short_urls = ShortURL.objects.all()
        serializer = ShortURLSerializer(short_urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShortURLDetail(APIView):
    def get_object(self, short_code):
        return get_object_or_404(ShortURL, short_code=short_code)

    def get(self, request, short_code):
        short_url = self.get_object(short_code)
        serializer = ShortURLSerializer(short_url)
        return Response(serializer.data)

    def put(self, request, short_code):
        short_url = self.get_object(short_code)
        serializer = ShortURLSerializer(short_url, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, short_code):
        short_url = self.get_object(short_code)
        short_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShortURLRedirect(APIView):
    def get(self, request, short_code):
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        short_url.access_count += 1
        short_url.save()
        return HttpResponseRedirect(short_url.url)

class ShortURLStats(APIView):
    def get(self, request, short_code):
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        serializer = ShortURLSerializer(short_url)
        return Response(serializer.data)