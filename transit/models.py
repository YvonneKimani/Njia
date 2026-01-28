from django.db import models

class Sacco(models.Model):
    name = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=15, default="999")
    harassment_hotline = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    landmark = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=100)
    route_number = models.CharField(max_length=10)
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE)
    stages = models.ManyToManyField(Stage, through='RouteStage')

    def __str__(self):
        return f"{self.route_number} ({self.sacco.name})"

class RouteStage(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    sequence_order = models.PositiveIntegerField()

    class Meta:
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.route.route_number} Stop: {self.stage.name}"

class FareSchedule(models.Model):
    TIME_SLOTS = [
        ('MORNING_PEAK', '6 AM - 10 AM'),
        ('OFF_PEAK', '10 AM - 4 PM'),
        ('EVENING_PEAK', '4 PM - 8 PM'),
        ('NIGHT', '8 PM - 6 AM'),
    ]
    route_stage = models.ForeignKey(RouteStage, on_delete=models.CASCADE, related_name='fares')
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    price = models.IntegerField()

    def __str__(self):
        return f"KES {self.price} ({self.time_slot})"

class FareReport(models.Model):
    route_stage = models.ForeignKey(RouteStage, on_delete=models.CASCADE, related_name='reports')
    reported_price = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reported_price} by {self.phone_number}"

class SafetyIncident(models.Model):
    INCIDENT_TYPES = [
        ('HARASSMENT', 'Harassment/Abuse'),
        ('EMERGENCY', 'General Emergency/Accident'),
        ('THEFT', 'Theft/Robbery'),
    ]
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='incidents')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    phone_number = models.CharField(max_length=15)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.incident_type} - {self.phone_number}"