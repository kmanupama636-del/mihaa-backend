from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer,OrderSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Order

@api_view(['POST'])
def create_order(request):

    name = request.data.get('name')
    price = request.data.get('price')
    quantity = request.data.get('quantity')
    image = request.data.get('image')

    Order.objects.create(
        name=name,
        price=price,
        quantity=quantity,
        image=image
    )

    return Response({"message": "Order created"})


@api_view(['POST'])
def signup(request):

    email=request.data.get('email')

    if User.objects.filter(email=email).exists():
        return Response({"error":"Email already exists"},status=400)

    user=User.objects.create_user(
        username=request.data.get('username'),
        email=email,
        password=request.data.get('password')
    )

    return Response({"message":"Account created"})


@api_view(['POST'])
def login(request):

    email=request.data.get('email')
    password=request.data.get('password')

    try:
        user=User.objects.get(email=email)
    except:
        return Response({"error":"User not found"},status=404)

    user=authenticate(username=user.username,password=password)

    if user:
        return Response({
            "id":user.id,
            "username":user.username,
            "email":user.email
        })

    return Response({"error":"Invalid password"})
# @api_view(['POST'])
# def signup(request):

#     username = request.data.get('username')
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if User.objects.filter(email=email).exists():
#         return Response({"error": "Email already exists"})

#     user = User.objects.create_user(
#         username=username,
#         email=email,
#         password=password
#     )

    # return Response({"message": "User created successfully"})
class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):

        queryset = Product.objects.all()

        category = self.request.query_params.get('category')

        if category is not None:
            queryset = queryset.filter(category_id=category)

        return queryset


class CategoryProductsView(ListAPIView):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer
@api_view(['GET'])
def get_orders(request):

    email = request.GET.get('email')

    orders = Order.objects.filter(email=email)

    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_order(request):

    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)
@api_view(['PUT'])
def update_order_status(request,id):

    order=Order.objects.get(id=id)
    order.status=request.data.get('status')
    order.save()

    return Response({"message":"Status Updated"})