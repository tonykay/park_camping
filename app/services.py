from typing import List, Dict
from datetime import timedelta
from datetime import date
from app.models import Park, Campground, Campsite, Availability
from app.mock_data import generate_mock_data

class DataService:
    def __init__(self):
        self.parks, self.campgrounds, self.campsites, self.availability = generate_mock_data()
        self.park_index = {p.id: p for p in self.parks}
        self.campground_index = {c.id: c for c in self.campgrounds}
        self.campsite_index = {s.id: s for s in self.campsites}
        # Map campground_id to list of campsites
        self.campground_sites = {}
        for site in self.campsites:
            self.campground_sites.setdefault(site.campground_id, []).append(site)
        # Map campsite_id to list of availability
        self.site_availability = {}
        for avail in self.availability:
            self.site_availability.setdefault(avail.campsite_id, []).append(avail)

    def campground_lister(self, park_id: str) -> List[Campground]:
        """
        List all campgrounds in a specified national park.
        Args:
            park_id: Unique identifier for the park
        Returns:
            List of Campground objects in the specified park
        """
        return [c for c in self.campgrounds if c.park_id == park_id]

    def availability_by_date(self, campground_id: str, start_date: date, nights: int) -> Dict[str, List[date]]:
        """
        Find available campsites for a specified date range.
        Args:
            campground_id: Unique identifier for the campground
            start_date: First night of the stay
            nights: Number of nights to stay
        Returns:
            Dictionary mapping campsite_id to a list of available dates
        """
        result = {}
        sites = self.campground_sites.get(campground_id, [])
        date_range = [start_date + timedelta(days=i) for i in range(nights)]
        for site in sites:
            avail_list = self.site_availability.get(site.id, [])
            available_dates = [
                a.date for a in avail_list
                if a.date in date_range and a.is_available
            ]
            if available_dates:
                result[site.id] = available_dates
        return result

    def cost_lister(self, campground_id: str) -> Dict[str, float]:
        """
        List all campsites in a campground with their costs.
        Args:
            campground_id: Unique identifier for the campground
        Returns:
            Dictionary mapping campsite_id to cost per night (in USD)
        """
        sites = self.campground_sites.get(campground_id, [])
        return {site.id: site.cost_per_night for site in sites}