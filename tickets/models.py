from django.db import models
class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN='open','Open'
        IN_PROGRESS='in_progress','In progress'
        RESOLVED='resolved','Resolved'
    class Priority(models.TextChoices):
        LOW='low','Low'; MEDIUM='medium','Medium'; HIGH='high','High'; URGENT='urgent','Urgent'
    customer_name=models.CharField(max_length=120)
    email=models.EmailField(blank=True)
    subject=models.CharField(max_length=220)
    message=models.TextField()
    category=models.CharField(max_length=80,default='General')
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    priority=models.CharField(max_length=12,choices=Priority.choices,default=Priority.MEDIUM)
    ai_summary=models.TextField(blank=True)
    ai_draft=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return f'#{self.pk} {self.subject}'
class TicketEvent(models.Model):
    ticket=models.ForeignKey(Ticket,related_name='events',on_delete=models.CASCADE)
    event_type=models.CharField(max_length=40)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
