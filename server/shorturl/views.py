# shortener/views.py

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShortURL
from .serializers import ShortURLSerializer
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


from django.views.generic import TemplateView

class IndexView(TemplateView):
    """
    Render the home page for creating short URLs.
    """
    template_name = 'index.html'

class StatsView(TemplateView):
    """
    Render the stats page for viewing URL statistics.
    """
    template_name = 'stats.html'



# API views using CBVs
class ShortURLListCreate(APIView):
    """
    CBV for listing all short URLs (GET) and creating a new short URL (POST).
    """
    def get(self, request):
        """
        Retrieve a list of all short URLs.
        """
        try:
            short_urls = ShortURL.objects.all()
            serializer = ShortURLSerializer(short_urls, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error retrieving short URLs: {str(e)}")
            return Response({"error": "Failed to retrieve short URLs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new short URL.
        """
        try:
            serializer = ShortURLSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print(f"Created short URL: {serializer.data['short_code']}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error creating short URL: {str(e)}")
            return Response({"error": "Failed to create short URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ShortURLDetail(APIView):
    """
    CBV for retrieving (GET), updating (PUT), and deleting (DELETE) a specific short URL.
    """
    def get_object(self, short_code):
        """
        Helper method to retrieve a ShortURL object by short_code.
        """
        return get_object_or_404(ShortURL, short_code=short_code)

    def get(self, request, short_code):
        """
        Retrieve details of a specific short URL.
        """
        try:
            short_url = self.get_object(short_code)
            serializer = ShortURLSerializer(short_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error retrieving short URL {short_code}: {str(e)}")
            return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, short_code):
        try:
            short_url = self.get_object(short_code)
            new_short_code = request.data.get('short_code')
            
            # Check for short code conflict if it’s changing
            if new_short_code and new_short_code != short_code:
                if ShortURL.objects.filter(short_code=new_short_code).exists():
                    return Response({"error": "Short code already exists"}, status=status.HTTP_400_BAD_REQUEST)
                short_url.short_code = new_short_code
            
            serializer = ShortURLSerializer(short_url, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(f"Updated short URL: {short_url.short_code}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error updating short URL {short_code}: {str(e)}")
            return Response({"error": "Failed to update short URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, short_code):
        """
        Delete a specific short URL.
        """
        try:
            short_url = self.get_object(short_code)
            short_url.delete()
            print(f"Deleted short URL: {short_code}")
            return Response({"message": "Short URL deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Error deleting short URL {short_code}: {str(e)}")
            return Response({"error": "Failed to delete short URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ShortURLRedirect(APIView):
    """
    CBV for redirecting a short URL to its original URL and incrementing access count.
    """
    def get(self, request, short_code):
        """
        Redirect to the original URL and increment the access count.
        """
        try:
            short_url = get_object_or_404(ShortURL, short_code=short_code)
            short_url.access_count += 1
            short_url.save()
            print(f"Redirected short URL {short_code}, new access count: {short_url.access_count}")
            return HttpResponseRedirect(short_url.url)
        except Exception as e:
            print(f"Error redirecting short URL {short_code}: {str(e)}")
            return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)

class ShortURLStats(APIView):
    """
    CBV for retrieving statistics of a specific short URL.
    """
    def get(self, request, short_code):
        """
        Retrieve statistics for a specific short URL.
        """
        try:
            short_url = get_object_or_404(ShortURL, short_code=short_code)
            serializer = ShortURLSerializer(short_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error retrieving stats for short URL {short_code}: {str(e)}")
            return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)