from django.core.management.base import BaseCommand
from tickets.models import Ticket,TicketEvent
SAMPLES=[
('Maya Patel','maya@example.test','Refund not received for order #QP-8821','I returned the item last week but my refund is not visible yet.','Billing','high','open'),
('Noah Williams','noah@example.test','Unable to reset account password','The reset link says it expired even though I opened it immediately.','Account access','medium','in_progress'),
('Priya Nair','priya@example.test','App crashes on checkout','The mobile app closes after I press confirm on checkout.','Technical issue','urgent','open'),
('Ethan Chen','ethan@example.test','Update delivery address','Can I change the address before the package is dispatched?','Orders','low','open'),
('Sofia Garcia','sofia@example.test','Duplicate charge on card','I can see two pending charges for the same purchase.','Billing','high','in_progress'),
('Arjun Rao','arjun@example.test','Need invoice for last month','Please send a copy of the invoice for my subscription.','Billing','low','resolved'),
('Olivia Brown','olivia@example.test','Two-factor code not arriving','I have tried several times but have not received the verification code.','Account access','medium','open')]
class Command(BaseCommand):
    help='Create synthetic demo tickets without deleting existing data.'
    def handle(self,*args,**kwargs):
        count=0
        for name,email,subject,message,category,priority,status in SAMPLES:
            t,created=Ticket.objects.get_or_create(subject=subject,defaults={'customer_name':name,'email':email,'message':message,'category':category,'priority':priority,'status':status})
            if created:TicketEvent.objects.create(ticket=t,event_type='created',description='Synthetic demo ticket created');count+=1
        self.stdout.write(self.style.SUCCESS(f'Created {count} demo tickets.'))
