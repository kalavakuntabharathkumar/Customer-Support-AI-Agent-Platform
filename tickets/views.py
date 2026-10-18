import json,os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Ticket,TicketEvent
from .agent import run_agent
@ensure_csrf_cookie
def dashboard(request):
    qs=Ticket.objects.all().order_by('-created_at')
    return render(request,'dashboard.html',{'tickets':qs[:60],'total_count':qs.count(),'open_count':qs.exclude(status='resolved').count(),'resolved_count':qs.filter(status='resolved').count(),'high_count':qs.filter(priority__in=['high','urgent']).exclude(status='resolved').count()})
@require_GET
def health(request): return JsonResponse({'ok':True,'service':'customer-support-agent','llm_configured':bool(os.getenv('LLM_API_KEY'))})
@require_GET
def ticket_api(request):
    results=[{'id':t.id,'subject':t.subject,'customer_name':t.customer_name,'category':t.category,'priority':t.priority,'status':t.status,'message':t.message,'ai_draft':t.ai_draft} for t in Ticket.objects.all().order_by('-created_at')[:100]]
    return JsonResponse({'results':results})
def payload(request):
    try: return json.loads(request.body.decode() or '{}')
    except (json.JSONDecodeError,UnicodeDecodeError): return {}
@require_POST
def agent_api(request):
    d=payload(request);tid=d.get('ticket_id')
    try: tid=int(tid) if tid is not None else None
    except (ValueError,TypeError): return JsonResponse({'ok':False,'error':'ticket_id must be an integer'},status=400)
    r=run_agent(str(d.get('message',''))[:4000],tid)
    return JsonResponse(r,status=200 if r.get('ok') else 400)
@require_POST
def reply_api(request,ticket_id):
    t=Ticket.objects.filter(pk=ticket_id).first()
    if not t: return JsonResponse({'ok':False,'error':'Ticket not found'},status=404)
    draft=str(payload(request).get('draft','')).strip()
    if not draft: return JsonResponse({'ok':False,'error':'Draft cannot be empty'},status=400)
    t.ai_draft=draft;t.save(update_fields=['ai_draft','updated_at'])
    TicketEvent.objects.create(ticket=t,event_type='draft_saved',description='Draft saved for human review; not sent')
    return JsonResponse({'ok':True,'sent':False})
