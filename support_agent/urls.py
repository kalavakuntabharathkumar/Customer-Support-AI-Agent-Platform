from django.contrib import admin
from django.urls import path
from tickets import views
urlpatterns=[path('admin/',admin.site.urls),path('',views.dashboard),path('api/health/',views.health),path('api/tickets/',views.ticket_api),path('api/agent/run/',views.agent_api),path('api/tickets/<int:ticket_id>/reply/',views.reply_api)]
