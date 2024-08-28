import datetime 

from django.contrib import admin
from django.db import models
from django.utils import timezone

class Location(models.Model):
    location_name = models.CharField("Location name", max_length=50)
    date_visited = models.DateTimeField("Date visited")
    
    def __str__(self):
        return self.location_name
    
    # customised display for admin location page for was_visited_recently   
    @admin.display(
        boolean=True,
        ordering="date_visited",
        description="Visited recently?"
    )
    def was_visited_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_visited <= now
    

class Event(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_name = models.CharField("Event name", max_length=50)
    date_visited = models.DateTimeField("Date visited")
    visit_counter = models.IntegerField("Number of event attendances", default=0)
    def __str__(self):
        return self.event_name
    
