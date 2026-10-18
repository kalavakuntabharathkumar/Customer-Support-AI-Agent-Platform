from .models import Ticket,TicketEvent
def get_ticket(ticket_id):
    t=Ticket.objects.filter(pk=ticket_id).first()
    if not t: return {'ok':False,'error':'Ticket not found'}
    return {'ok':True,'ticket':{'id':t.id,'subject':t.subject,'customer':t.customer_name,'category':t.category,'priority':t.priority,'status':t.status,'message':t.message}}
def search_tickets(query,limit=8):
    qs=Ticket.objects.filter(subject__icontains=query)|Ticket.objects.filter(message__icontains=query)
    results=[{'id':t.id,'subject':t.subject,'status':t.status,'priority':t.priority} for t in qs.order_by('-created_at')[:max(1,min(int(limit),20))]]
    return {'ok':True,'results':results}
def draft_reply(ticket_id,tone='professional'):
    t=Ticket.objects.filter(pk=ticket_id).first()
    if not t: return {'ok':False,'error':'Ticket not found'}
    t.ai_draft=f'Hello {t.customer_name},\\n\\nThank you for contacting us about “{t.subject}”. We understand your concern and are reviewing the details. If you have a relevant order or reference number, please share it so we can investigate. Our team will follow up with next steps.\\n\\nRegards,\\nCustomer Support'
    t.save(update_fields=['ai_draft','updated_at'])
    TicketEvent.objects.create(ticket=t,event_type='drafted',description='Draft created for human review; not sent')
    return {'ok':True,'draft':t.ai_draft,'sent':False}
def resolve_ticket(ticket_id,resolution_note):
    t=Ticket.objects.filter(pk=ticket_id).first()
    if not t: return {'ok':False,'error':'Ticket not found'}
    if not resolution_note.strip(): return {'ok':False,'error':'Resolution note required'}
    t.status=Ticket.Status.RESOLVED
    t.save(update_fields=['status','updated_at'])
    TicketEvent.objects.create(ticket=t,event_type='resolved',description=resolution_note[:2000])
    return {'ok':True,'status':t.status}
TOOL_REGISTRY={'get_ticket':get_ticket,'search_tickets':search_tickets,'draft_reply':draft_reply,'resolve_ticket':resolve_ticket}
def run_tool(name,arguments):
    if name not in TOOL_REGISTRY: return {'ok':False,'error':'Unknown tool'}
    try: return TOOL_REGISTRY[name](**arguments)
    except (TypeError,ValueError) as e: return {'ok':False,'error':str(e)}
