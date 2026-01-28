from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RouteStage, Sacco, FareReport, SafetyIncident
from .services import get_fare_info
from .utils import send_fare_summary_sms, send_emergency_alert, send_custom_sms

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
        response += "3. Safety & Emergency"

    elif levels[0] == "1":
        if len(levels) == 1:
            response = "CON Destination stage:"
        elif len(levels) == 2:
            route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
            if route_stops.exists():
                response = "CON Select Route:\n"
                for i, rs in enumerate(route_stops[:5]):
                    response += f"{i+1}. {rs.route.route_number} ({rs.route.sacco.name})\n"
            else:
                response = "END No routes found."
        elif len(levels) == 3:
            route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
            selected = route_stops[int(levels[2])-1]
            price, status = get_fare_info(selected)
            response = f"END {selected.route.number}\nFare: KES {price} ({status})\nSMS Sent."
            send_fare_summary_sms(phone_number, selected.route.number, price, selected.stage.name)

    elif levels[0] == "2":
        if len(levels) == 1:
            response = "CON Destination for report:"
        elif len(levels) == 2:
            route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
            response = "CON Select Route:\n"
            for i, rs in enumerate(route_stops[:5]):
                response += f"{i+1}. {rs.route.route_number}\n"
        elif len(levels) == 3:
            response = "CON Enter price paid:"
        elif len(levels) == 4:
            route_stops = RouteStage.objects.filter(stage__name__icontains=levels[1])
            selected = route_stops[int(levels[2])-1]
            FareReport.objects.create(route_stage=selected, reported_price=int(levels[3]), phone_number=phone_number)
            response = "END Thank you. Report received."
            send_custom_sms(phone_number, f"Njia: Report for {selected.route.number} recorded. Thanks for helping!")

    elif levels[0] == "3":
        if len(levels) == 1:
            response = "CON Safety Menu:\n1. Emergency (999)\n2. Report Harassment"
        elif levels[1] == "1":
            sacco = Sacco.objects.first()
            response = "END Emergency Alert Sent."
            send_emergency_alert(phone_number, sacco.name, sacco.emergency_contact)
        elif levels[1] == "2":
            if len(levels) == 2:
                response = "CON Select Sacco:\n"
                for i, s in enumerate(Sacco.objects.all()[:5]):
                    response += f"{i+1}. {s.name}\n"
            elif len(levels) == 3:
                sacco = Sacco.objects.all()[int(levels[2])-1]
                SafetyIncident.objects.create(sacco=sacco, incident_type='HARASSMENT', phone_number=phone_number)
                response = f"END Report sent to {sacco.name}. Hotline: {sacco.harassment_hotline}"
                send_custom_sms(phone_number, f"Njia: Harassment report for {sacco.name} logged. Hotline: {sacco.harassment_hotline}")

    return HttpResponse(response, content_type='text/plain')