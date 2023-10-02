from django.urls import path

from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    # path('confirm_payment/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('order_complete', views.order_complete, name='order_complete'),
]