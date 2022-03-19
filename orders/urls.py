from . import views
from django.urls import path

urlpatterns = [
    path('', views.OrderCreateListView.as_view(), name="orders"),
    path('<str:order_id>/', views.OrderDetailView.as_view(), name="order_detail"),
    path('update-order-status/<str:order_id>/', views.UpdateOrderStatus.as_view(), name="update_order_status"),
    path('user/<str:user_id>/', views.UserOrdersView.as_view(), name="user_orders"),
    path('user/<str:user_id>/order/<str:order_id>/', views.UserOrderDetail.as_view(), name="user_order"),
    path('user/<str:user_id>/orders/', views.DeleteAllUserOrders.as_view(), name="user_orders_delete"),
]
