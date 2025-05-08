from typing import List, Tuple, Dict
from datetime import datetime, date
from pydantic import BaseModel, Field


class Park(BaseModel):
    id: str  # Unique identifier
    name: str  # Park name
    description: str  # Brief description
    location: str  # General location
    established_date: datetime  # When the park was established
    size_acres: int  # Size in acres
    visitor_centers: List[str]  # Names of visitor centers


class Campground(BaseModel):
    id: str  # Unique identifier
    park_id: str  # Reference to parent park
    name: str  # Campground name
    description: str  # Brief description
    location: str  # Location within the park
    elevation_ft: int  # Elevation in feet
    num_sites: int  # Total number of campsites
    amenities: List[str]  # Available amenities (restrooms, showers, etc.)
    season: Tuple[str, str]  # Operating season (start_month, end_month)


class Campsite(BaseModel):
    id: str  # Unique identifier
    campground_id: str  # Reference to parent campground
    site_number: str  # Site identifier (e.g., "A12")
    site_type: str  # Type of site (tent, RV, group, etc.)
    max_occupancy: int  # Maximum number of people
    max_vehicles: int  # Maximum number of vehicles
    accessible: bool  # ADA accessible
    power_hookups: bool  # Has electrical hookups
    water_hookups: bool  # Has water hookups
    sewer_hookups: bool  # Has sewer hookups
    cost_per_night: float  # Cost in USD


class Availability(BaseModel):
    campsite_id: str  # Reference to campsite
    date: date  # Specific date
    is_available: bool  # Whether the site is available
    is_reserved: bool  # Whether the site is reserved