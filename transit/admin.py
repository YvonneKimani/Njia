from django.contrib import admin
from .models import Sacco, Stage, Route, RouteStage, FareSchedule, FareReport, SafetyIncident, LostItem

class FareScheduleInline(admin.TabularInline):
    model = FareSchedule
    extra = 4 

class RouteStageInline(admin.TabularInline):
    model = RouteStage
    extra = 1
    autocomplete_fields = ['stage']

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'landmark')
    search_fields = ('name',)

@admin.register(Sacco)
class SaccoAdmin(admin.ModelAdmin):
    list_display = ('name', 'emergency_contact', 'harassment_hotline')
    search_fields = ('name',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_number', 'name', 'sacco')
    list_filter = ('sacco',)
    search_fields = ('route_number', 'name')
    inlines = [RouteStageInline]

@admin.register(RouteStage)
class RouteStageAdmin(admin.ModelAdmin):
    list_display = ('route', 'stage', 'sequence_order')
    list_filter = ('route', 'stage')
    inlines = [FareScheduleInline]

@admin.register(FareReport)
class FareReportAdmin(admin.ModelAdmin):
    list_display = ('route_stage', 'reported_price', 'phone_number', 'timestamp')
    list_filter = ('route_stage__route', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(SafetyIncident)
class SafetyIncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_type', 'sacco', 'phone_number', 'timestamp')
    list_filter = ('incident_type', 'sacco', 'timestamp')
    search_fields = ('phone_number', 'details')
    readonly_fields = ('timestamp',)

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'sacco', 'plate_number', 'user_phone', 'is_resolved', 'created_at')
    list_filter = ('sacco', 'is_resolved', 'created_at')
    search_fields = ('user_phone', 'description', 'plate_number')
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at',)