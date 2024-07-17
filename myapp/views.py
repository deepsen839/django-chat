from django.shortcuts import render
from .models import Status
from django.http import JsonResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def update_status(request):
    try:
        channel_layer = get_channel_layer()
        if request.method=='POST':
            data = json.loads(request.body)
            record = Status.objects.get()
            record.status= not record.status
            record.save()
            record = Status.objects.get()
            async_to_sync(channel_layer.group_send)(
            "active_users",
            {
                "type": "user_active",
                "status":record.status,
            }
        )
            return JsonResponse({'status':record.status})
        return render(request,'chat.html')
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error occured'})
    
def index(request):
    return render(request,'index.html')    