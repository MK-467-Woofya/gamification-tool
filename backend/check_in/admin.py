from django.contrib import admin
"""
Admin dashboard behaviour for check_in entities
"""

# Register your models here.
from .models import Location, Event

# Inline method for adding Events to Locations in admin, use admin.StackedInline if want expanded view of inline
class EventInline(admin.TabularInline):
    model = Event
    extra = 2

# user specified admin page for location operations
class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["location_name"]}), 
        ("Date information", {"fields": ["date_visited"], "classes": ["collapse"]}),
    ]
    inlines = [EventInline]
    
    # display custom attributes at location admin page, instead of just location_name
    list_display = ["location_name", "date_visited", "was_visited_recently"]
    
    # add a sidebar filter
    list_filter = ["date_visited"]
    
    # add a search field
    search_fields = ["location_name"]

admin.site.register(Location, LocationAdmin)

# auto-generated admin actions page for events - included in Location admin instead
## admin.site.register(Event)