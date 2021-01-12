from sit.models import Sit
from sit.serializers import SitSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class SitList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Sit.objects.all()
        serializer = SitSerializer(snippets, many=True)
        return Response(serializer.data)


