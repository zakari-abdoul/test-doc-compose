from rest_framework.decorators import action

from app.models import App
from app.serializers import AppSerializer, AppDomaineSerializer, AppDomainesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


class AppList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = App.objects.all()
        serializer = AppSerializer(snippets, many=True)
        return Response(serializer.data)




class AppViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['get'], serializer_class=AppDomainesSerializer)
    def app_domaine(self, request, *args, **kwargs):
        """
         connection with username and password
        """
        user = self.get_object()
        serializer = AppDomainesSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
class AppDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return App.objects.get(pk=pk)
        except App.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AppSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AppSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)