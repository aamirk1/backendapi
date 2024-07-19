from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models,serializers
from django.db.models import Count
import random

# Create your views here.
class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    def get_queryset(self):
        queryset = models.Category.objects.all();
        queryset = queryset.annotate(random_order = Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]
    

class BrandList(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()

    
class ProductList(generics.ListAPIView):

    serializer_class = serializers.ProductSerializer
    def get_queryset(self):
        queryset = models.Product.objects.all();
        queryset = queryset.annotate(random_order = Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    
    
class PopularProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    def get_queryset(self):
        queryset = models.Product.objects.filter(ratings__gte = 4.0, ratings__lte = 5.0);
        queryset = queryset.annotate(random_order = Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    

class ProductListByClothesType(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    def get_queryset(self,request):
        query = request.query_params.get('clothsType')
        if query:
            queryset = models.Product.objects.filter(clothsType = query);
            queryset = queryset.annotate(random_order = Count('id'))
            product_list = list(queryset)
            random.shuffle(product_list)
            limited_products = product_list[:20]
            serializer = serializers.ProductSerializer(limited_products,many = True);
            return Response(serializer.data)
        else:
            return Response({"message": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)



class SimilarProduct(APIView):
    def get(self, request):
        query = request.query_params.get('category_id', None)
        if query:
            products = models.Product.objects.filter(category = query);
            product_list = list(products)
            random.shuffle(product_list)
            limited_product = product_list[:6]
            serializer = serializers.ProductSerializer(limited_product,many = True);
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        

class SearchProductByTitle(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)
        if query:
            products = models.Product.objects.filter(title_icontains = query);
            
            serializer = serializers.ProductSerializer(products,many = True);
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class FilterProductByCategory(APIView):
    def get(self,request):
        query = request.quert_params.get('category',None)
        if query:
            products = models.Product.objects.filter(category = query);
            serializer = serializers.ProductSerializer(products, many = True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        
