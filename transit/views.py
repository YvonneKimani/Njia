from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RouteStage, Sacco, FareReport, SafetyIncident, LostItem
from .services import get_fare_info
from .utils import *

@csrf_exempt
def ussd_callback(request):
    text = request.POST.get("text", "")
    phone_number = request.POST.get("phoneNumber")
    levels = text.split("*")
    response = ""

    if text == "":
        response = "CON Karibu Njia\n"
        response += "1. Find Route & Fare\n"
        response += "2. Report Price Hike\n"
        response += "3. Safety & Emergency\n"
        response += "4. Lost & Found"

    elif levels[0] == "1":
        if len(levels) == 1:
            response = "CON Enter destination stage name:"
        elif len(levels) == 2:
            route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
            if route_stops.exists():
                response = "CON Select Route:\n"
                for i, rs in enumerate(route_stops[:5]):
                    response += f"{i+1}. {rs.route.route_number} ({rs.route.sacco.name})\n"
            else:
                response = "END No routes found for that destination."
        elif len(levels) == 3:
            try:
                route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
                selected = route_stops[int(levels[2])-1]
                boarding = RouteStage.objects.filter(route=selected.route).order_by('sequence_order').first()
                price, status = get_fare_info(selected)
                
                response = f"END [NJIA TRIP INFO]\n"
                response += f"Route: {selected.route.route_number} ({selected.route.sacco.name})\n"
                response += f"Board: {boarding.stage.name}\n"
                response += f"Drop: {selected.stage.name}\n"
                response += f"Fare: KES {price} ({status})\n"
                response += f"----------------\n"
                response += f"SMS summary sent."
                
                try:
                    send_fare_summary_sms(phone_number, selected.route.route_number, price, selected.stage.name, boarding.stage.name)
                except Exception: pass
            except Exception:
                response = "END Error retrieving route details."

    elif levels[0] == "2":
        if len(levels) == 1:
            response = "CON Stage name for report:"
        elif len(levels) == 2:
            route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
            if route_stops.exists():
                response = "CON Select Route:\n"
                for i, rs in enumerate(route_stops[:5]):
                    response += f"{i+1}. {rs.route.route_number}\n"
            else:
                response = "END No routes found."
        elif len(levels) == 3:
            response = "CON Enter price paid (KES):"
        elif len(levels) == 4:
            try:
                route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
                selected = route_stops[int(levels[2])-1]
                FareReport.objects.create(route_stage=selected, reported_price=int(levels[3]), phone_number=phone_number)
                response = "END [NJIA REPORT]\nThank you! Your report helps maintain fair prices for everyone."
                try:
                    send_custom_sms(phone_number, f"Njia: Fare report for {selected.route.route_number} recorded.")
                except Exception: pass
            except Exception:
                response = "END Error saving report."

    elif levels[0] == "3":
        if len(levels) == 1:
            response = "CON 1. Emergency (999)\n2. Report Harassment\n3. Report Theft"
        elif levels[1] == "1":
            sacco = Sacco.objects.first()
            response = "END Emergency Alert Sent."
            send_emergency_alert(phone_number, sacco.name, sacco.emergency_contact)
        elif levels[1] in ["2", "3"]:
            incident_type = 'HARASSMENT' if levels[1] == "2" else 'THEFT'
            if len(levels) == 2:
                response = "CON Select Sacco:\n"
                for i, s in enumerate(Sacco.objects.all()[:5]):
                    response += f"{i+1}. {s.name}\n"
            elif len(levels) == 3:
                response = f"CON Describe the {incident_type.lower()}:"
            elif len(levels) == 4:
                try:
                    sacco = Sacco.objects.all()[int(levels[2])-1]
                    SafetyIncident.objects.create(sacco=sacco, incident_type=incident_type, phone_number=phone_number, details=levels[3])
                    response = f"END Report Logged.\nHotline: {sacco.harassment_hotline}"
                    send_custom_sms(phone_number, f"Njia: {incident_type} report for {sacco.name} logged.")
                except Exception:
                    response = "END Error logging report."

    elif levels[0] == "4":
        if len(levels) == 1:
            response = "CON 1. Report Lost Item\n2. Sacco Contacts"
        elif levels[1] == "1":
            if len(levels) == 2:
                response = "CON Describe the item:"
            elif len(levels) == 3:
                response = "CON Enter Plate No (or NA):"
            elif len(levels) == 4:
                response = "CON Select Sacco:\n"
                for i, s in enumerate(Sacco.objects.all()[:5]):
                    response += f"{i+1}. {s.name}\n"
            elif len(levels) == 5:
                try:
                    sacco = Sacco.objects.all()[int(levels[4])-1]
                    LostItem.objects.create(user_phone=phone_number, sacco=sacco, description=levels[2], plate_number=levels[3])
                    response = f"END [LOGGED]\nCall {sacco.name} at {sacco.emergency_contact} to verify."
                    send_lost_item_request_sms(phone_number, sacco.name, sacco.emergency_contact)
                except Exception:
                    response = "END Error processing lost item."
        elif levels[1] == "2":
            response = "CON Select Sacco:\n"
            for i, s in enumerate(Sacco.objects.all()[:5]):
                response += f"{i+1}. {s.name}\n"
            if len(levels) == 3:
                sacco = Sacco.objects.all()[int(levels[2])-1]
                response = f"END {sacco.name} Contact: {sacco.emergency_contact}"

    return HttpResponse(response, content_type='text/plain')