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
        f"NJIA EMERGENCY ALERT\n"
        f"Sacco: {sacco_name}\n"
        f"Sacco Hotline: {sacco_phone}\n"
        f"National Police: 999\n"
        f"Please stay in a well-lit area."
    )
    send_custom_sms(phone_number, message)

def send_fare_summary_sms(phone_number, route, price, drop_stage, board_stage):
    message = (
        f"NJIA TRIP SUMMARY\n"
        f"Route: {route}\n"
        f"Boarding: {board_stage}\n"
        f"Alighting: {drop_stage}\n"
        f"Current Fare: KES {price}\n"
        f"Safe Journey!"
    )
    send_custom_sms(phone_number, message)

def send_lost_item_request_sms(phone_number, sacco_name, sacco_contact):
    message = (
        f"NJIA LOST & FOUND\n"
        f"Your inquiry for {sacco_name} has been logged.\n"
        f"Next Steps: Call {sacco_contact} to verify your item.\n"
        f"Phone Reference: {phone_number}"
    )
    send_custom_sms(phone_number, message)