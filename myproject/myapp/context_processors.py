# context_processors.py
from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-notification_date')[:5]
    else:
        notifications = []
    return {
        'notifications': notifications
    }
