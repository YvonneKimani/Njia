from django.core.management.base import BaseCommand
from transit.models import Sacco, Stage, Route, RouteStage, FareSchedule

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Seeding Nairobi Transit Data...")

        # 1. Define Saccos
        saccos_data = [
            {"name": "Super Metro", "emergency": "0700123456", "harassment": "0800111222"},
            {"name": "2NK Sacco", "emergency": "0706235260", "harassment": "0706235261"},
            {"name": "Forward Travellers", "emergency": "0735963532", "harassment": "0735963533"},
            {"name": "Ngong Travellers", "emergency": "0722000111", "harassment": "0722000112"},
            {"name": "Kikuyu Sacco", "emergency": "0733444555", "harassment": "0733444556"},
        ]

        saccos = {}
        for s in saccos_data:
            obj, _ = Sacco.objects.get_or_create(
                name=s["name"], 
                emergency_contact=s["emergency"],
                harassment_hotline=s["harassment"]
            )
            saccos[s["name"]] = obj

        # 2. Define Common Stages
        stages_list = [
            ("CBD-Commercial", "Near Tom Mboya St"),
            ("CBD-Railways", "Haile Selassie Ave"),
            ("T-Mall", "Langata Rd Junction"),
            ("MMU", "Multimedia University Gate"),
            ("Rongai", "Tuskys Stage"),
            ("Karen", "Karen Shopping Centre"),
            ("Ngong", "Ngong Bus Terminus"),
            ("Githurai", "Thika Road Footbridge"),
            ("Uthiru", "Waiyaki Way"),
            ("Kikuyu", "Kikuyu Town Bus Park")
        ]

        stages = {}
        for name, landmark in stages_list:
            obj, _ = Stage.objects.get_or_create(name=name, landmark=landmark)
            stages[name] = obj

        # 3. Define Routes and Fares
        routes_data = [
            {
                "num": "125", "sacco": "Super Metro", "dest": "Rongai",
                "stops": [
                    ("CBD-Railways", 1, 50, 30, 80, 50),
                    ("T-Mall", 2, 60, 40, 90, 60),
                    ("MMU", 3, 80, 50, 100, 70),
                    ("Rongai", 4, 100, 70, 120, 80),
                ]
            },
            {
                "num": "111", "sacco": "Ngong Travellers", "dest": "Ngong",
                "stops": [
                    ("CBD-Railways", 1, 50, 30, 70, 50),
                    ("Karen", 2, 70, 50, 100, 70),
                    ("Ngong", 3, 100, 60, 120, 80),
                ]
            },
            {
                "num": "45", "sacco": "Forward Travellers", "dest": "Githurai",
                "stops": [
                    ("CBD-Commercial", 1, 30, 20, 50, 30),
                    ("Githurai", 2, 60, 40, 80, 50),
                ]
            },
            {
                "num": "105", "sacco": "Kikuyu Sacco", "dest": "Kikuyu",
                "stops": [
                    ("CBD-Commercial", 1, 40, 30, 60, 40),
                    ("Uthiru", 2, 60, 40, 80, 50),
                    ("Kikuyu", 3, 80, 50, 100, 70),
                ]
            }
        ]

        for r in routes_data:
            route_obj, _ = Route.objects.get_or_create(
                route_number=r["num"], 
                sacco=saccos[r["sacco"]],
                name=f"{r['sacco']} {r['num']}"
            )
            
            for stop_name, order, morning, off, evening, night in r["stops"]:
                rs, _ = RouteStage.objects.get_or_create(
                    route=route_obj,
                    stage=stages[stop_name],
                    sequence_order=order
                )
                
                # Create the 4 Time Slots for each stop
                fares = [
                    ('MORNING_PEAK', morning),
                    ('OFF_PEAK', off),
                    ('EVENING_PEAK', evening),
                    ('NIGHT', night)
                ]
                
                for slot, price in fares:
                    FareSchedule.objects.get_or_create(route_stage=rs, time_slot=slot, price=price)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 5 Nairobi routes!"))