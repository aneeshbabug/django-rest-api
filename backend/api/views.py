from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Item
from .serializer import Itemgetserializer, Itemserializer,BackendUserSerializer
from .permissions import IsAdmin, IsOwner

# Create your views here.
def home(request):
    return HttpResponse('Welcome to REST API')

class RegisterBackendUserView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = BackendUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User added Successfully'}, status=201)
        return Response({'message': 'Data Invalid', 'errors': serializer.errors}, status=400)

class ItemListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Item.objects.all()
        serializer = Itemgetserializer(queryset, many=True)
        response = Response(serializer.data)
        return response

    def post(self,request):
        serializer = Itemserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message':'Data Saved Successfully'},status=201)
        return Response({'message':'Data Invalid','errors': serializer.errors},status=400)

class ItemDetailView(APIView):

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAuthenticated(), IsAdmin(), IsOwner()]
        return [IsAuthenticated()]

    def get(self,request,id):
        item = get_object_or_404(Item, id=id)
        serializer = Itemgetserializer(item)
        response = Response(serializer.data)
        return response

    def put(self,request,id):
        item = get_object_or_404(Item, id=id)
        serializer = Itemserializer(item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Fully Changed Successfully'},status=200)
        return Response({'message':'Data Invalid','errors': serializer.errors},status=400)

    def patch(self,request,id):
        item = get_object_or_404(Item, id=id)
        serializer = Itemserializer(item,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Partially Changed Successfully'},status=200)
        return Response({'message':'Data Invalid','errors': serializer.errors},status=400)

    def delete(self,request,id):
        item = get_object_or_404(Item, id=id)
        item.delete()
        return Response({'message': 'Data deleted Successfully'}, status=200)




