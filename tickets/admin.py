from django.contrib import admin
from .models import Ticket,TicketEvent
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display=('id','subject','customer_name','category','priority','status','created_at')
    list_filter=('status','priority','category')
    search_fields=('subject','customer_name','message')
admin.site.register(TicketEvent)
