import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Location

class LocationModelTests(TestCase):
    def test_was_visited_recently_with_future_date_visited(self):
        """
        was_visited_recently() returns False for locations whose date_visited is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_location_visit = Location(date_visited=time)
        self.assertIs(future_location_visit.was_visited_recently(), False)
        
    def test_was_visited_recently_with_old_date_visited(self):
        """
        was_visited_recently() returns False for locations whose date_visited is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_visit = Location(date_visited=time)
        self.assertIs(old_visit.was_visited_recently(), False)
        
    def test_was_visited_recently_with_recent_date_visited(self):
        """
        was_visited_recently() returns True for locations whose date_visited is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_visit = Location(date_visited=time)
        self.assertIs(recent_visit.was_visited_recently(), True)
   
# Mock location object function for views testing     
def create_location(location_name, days):
    """
    Create a location with the given 'location_name' and date_visited 
    offset to now (negative for visits in the past, positive for visits that have yet to occur)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Location.objects.create(location_name=location_name,date_visited=time)

# Index View testing classes
class LocationIndexViewTests(TestCase):
    def test_no_locations(self):
        """
        If no locations exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("check_in:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events are available")
        self.assertQuerySetEqual(response.context["latest_locations_list"], [])
        
    
    def test_past_location(self):
        """
        locations with a date_visited in the past are displayed on the
        index page.
        """
        location = create_location(location_name="Past location.", days=-30)
        response = self.client.get(reverse("check_in:index"))
        self.assertQuerySetEqual(
            response.context["latest_location_list"],
            [location],
        )

    def test_future_location(self):
        """
        locations with a date_visited in the future aren't displayed on
        the index page.
        """
        create_location(location_name="Future location.", days=30)
        response = self.client.get(reverse("check_in:index"))
        self.assertContains(response, "No check_in are available.")
        self.assertQuerySetEqual(response.context["latest_location_list"], [])

    def test_future_location_and_past_location(self):
        """
        Even if both past and future locations exist, only past locations
        are displayed.
        """
        location = create_location(location_name="Past location.", days=-30)
        create_location(location_name="Future location.", days=30)
        response = self.client.get(reverse("check_in:index"))
        self.assertQuerySetEqual(
            response.context["latest_location_list"],
            [location],
        )

    def test_two_past_locations(self):
        """
        The locations index page may display multiple locations.
        """
        location1 = create_location(location_name="Past location 1.", days=-30)
        location2 = create_location(location_name="Past location 2.", days=-5)
        response = self.client.get(reverse("check_in:index"))
        self.assertQuerySetEqual(
            response.context["latest_location_list"],
            [location2, location1],
        )

# Detail view testing class       
class LocationDetailViewTests(TestCase):
    def test_future_location(self):
        """
        The detail view of a location with a pub_date in the future
        returns a 404 not found.
        """
        future_location = create_location(location_name="Future location.", days=5)
        url = reverse("check_in:detail", args=(future_location.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_location(self):
        """
        The detail view of a location with a pub_date in the past
        displays the location's text.
        """
        past_location = create_location(location_name="Past Location.", days=-5)
        url = reverse("check_in:detail", args=(past_location.id,))
        response = self.client.get(url)
        self.assertContains(response, past_location.location_name)