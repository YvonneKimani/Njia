from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg
import pytz
from .models import FareReport

def get_current_time_slot():
    nairobi_tz = pytz.timezone('Africa/Nairobi')
    hour = datetime.now(nairobi_tz).hour
    
    if 6 <= hour < 10: return 'MORNING_PEAK'
    if 10 <= hour < 16: return 'OFF_PEAK'
    if 16 <= hour < 20: return 'EVENING_PEAK'
    return 'NIGHT'

def get_fare_info(route_stage_obj):
    recent_reports = FareReport.objects.filter(
        route_stage=route_stage_obj,
        timestamp__gte=timezone.now() - timedelta(hours=2)
    )
    
    if recent_reports.exists():
        avg_price = recent_reports.aggregate(Avg('reported_price'))['reported_price__avg']
        return int(avg_price), "Live"

    slot = get_current_time_slot()
    fare = route_stage_obj.fares.filter(time_slot=slot).first()
    
    if fare:
        return fare.price, slot.replace("_", " ").title()
    return 0, "Default"