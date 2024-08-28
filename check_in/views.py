from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Location, Event

"""
Check_in views handle application logic and functionality.
This is where we will put API views
"""

## Generic index view
class IndexView(generic.ListView):
    template_name = "check_in/index.html"
    # Tell Django to use latest_locations_list instead of the auto-generated full list of locations
    context_object_name = "latest_locations_list"
    
    def get_queryset(self):
        return Location.objects.filter(date_visited__lte=timezone.now()).order_by("-date_visited")[:5]

## Non-generic index view
#def index(request):
#    latest_locations_list = Location.objects.order_by("-date_visited")[:5]
#    template = loader.get_template("check_in/index.html")
#    context = {"latest_locations_list": latest_locations_list}
#    return render(request, "check_in/index.html", context)

## Generic detail view
class DetailView(generic.DetailView):
    model = Location
    template_name = "check_in/detail.html"
    
    def get_queryset(self):
        """
        Excludes any location visits that are in the future - lte = less than or equal to
        """
        return Location.objects.filter(date_visited__lte=timezone.now())

## Non-generic detail view    
#def detail(request, location_id):
#    location = get_object_or_404(Location, pk=location_id)
#    return render(request, "check_in/detail.html", {"location": location})

## Generic result view
class ResultsView(generic.DetailView):
    model = Location
    template_name = "check_in/results.html"

## Non-generic results view
#def results(request, location_id):
#    location = get_object_or_404(Location, pk=location_id)
#    return render(request, "check_in/results.html", {"location": location})

## Non-generic visit event view
def visit_event(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    try:
        selected_event = location.event_set.get(pk=request.POST["event"])
    except (KeyError, Event.DoesNotExist):
        # Redisplay the voting form
        return render(
            "check_in/detail.html",
            {
                "location": location,
                "error_message": "No event was selected.",
            },
        )
    else:
        selected_event.visit_counter = F("visit_counter") + 1
        selected_event.save()
    
    return HttpResponseRedirect(reverse("check_in:results", args=(location.id,)))