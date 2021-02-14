from django.urls import path

from . views import (
	home,
	products,
	customer,
	createOrder,
	updateOrder,
	deleteOrder,
	registerPage,
	loginPage,
	logoutUser,
)

app_name = 'accounts'

urlpatterns = [
    path('', home, name="home"),
    path('products/', products, name="products"),
    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', loginPage, name="logout"),
    path('create_order/<int:pk>/', createOrder, name="create_order"),
    path('update_order/<int:pk>/', updateOrder, name="update"),
    path('delete_order/<int:pk>/', deleteOrder, name="delete"),
    path('customers/<int:pk>/', customer, name="customer"),
]
