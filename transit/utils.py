import africastalking
from django.conf import settings

africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
sms = africastalking.SMS

def send_custom_sms(phone_number, message):
    try:
        sms.send(message, [phone_number])
    except Exception:
        pass

def send_emergency_alert(phone_number, sacco_name, sacco_phone):
    message = (
        f"[NJIA EMERGENCY]\n"
        f"Alert triggered for {sacco_name}.\n"
        f"Hotline: {sacco_phone}\n"
        f"Police: 999"
    )
    send_custom_sms(phone_number, message)

def send_fare_summary_sms(phone_number, route, price, stage):
    message = (
        f"Njia Trip Summary:\n"
        f"Route: {route}\n"
        f"Dest: {stage}\n"
        f"Fare: KES {price}"
    )
    send_custom_sms(phone_number, message)