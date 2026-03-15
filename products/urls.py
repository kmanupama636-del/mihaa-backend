from django.urls import path
from .views import CategoryProductsView
from .views import signup,login,ProductViewSet
from .views import create_order,get_orders
from .import views
product_list=ProductViewSet.as_view({'get':'list'})
urlpatterns = [

path('categories/', CategoryProductsView.as_view()),
path('products/', product_list),
path('api/signup/', signup),
path('api/login/', login),
path('orders/',views.get_orders),
path('orders/create/',views.create_order),
path('orders/update/<int:id>/',views.update_order_status),
]