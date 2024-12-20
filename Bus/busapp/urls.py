from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('add_bus/', add_bus, name='add_bus'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('client/', views.client_page, name='client'), 
    path('company/', views.company_page, name='company'),
    path('edit_bus/', views.edit_bus, name='edit_bus'),
    path('delete_bus/<int:bus_id>/', delete_bus, name='delete_bus'),
    path('calculate_cost/<int:bus_id>/', views.calculate_cost, name='calculate_cost'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('profile/', views.profile, name='profile'),
    path('update-accept-client/<int:order_id>/', update_accept_client, name='update_accept_client'),
    path('order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    path('leave-review/', views.leave_review, name='leave_review'),
    path('reply-to-review/<int:review_id>/', reply_to_review, name='reply_to_review'),
    path('bus_details/<int:bus_id>/', views.bus_details, name='bus_details'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)