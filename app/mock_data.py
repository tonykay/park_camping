import random
import string
from datetime import datetime, timedelta, date
from typing import List, Tuple
from app.models import Park, Campground, Campsite, Availability

PARK_NAMES = [
    "Redwood Valley National Park",
    "Crystal Lake Reserve",
    "Sunset Canyon Park",
    "Eagle Ridge National Park",
    "Blue River Wilderness"
]

CAMP_AMENITIES = [
    "restrooms", "showers", "picnic tables", "fire rings", "water spigots", "dump station"
]

SITE_TYPES = ["tent", "RV", "group", "cabin"]

def random_id(prefix: str, length: int = 6) -> str:
    return f"{prefix}_{''.join(random.choices(string.ascii_uppercase + string.digits, k=length))}"

def generate_mock_parks(n: int) -> List[Park]:
    parks = []
    for i in range(n):
        park = Park(
            id=random_id("park"),
            name=PARK_NAMES[i % len(PARK_NAMES)],
            description=f"A beautiful national park known for its {random.choice(['forests', 'lakes', 'mountains', 'wildlife', 'scenic views'])}.",
            location=random.choice(["North", "South", "East", "West", "Central"]) + " Region",
            established_date=datetime(1950 + random.randint(0, 70), random.randint(1, 12), random.randint(1, 28)),
            size_acres=random.randint(50000, 500000),
            visitor_centers=[f"Visitor Center {j+1}" for j in range(random.randint(1, 3))]
        )
        parks.append(park)
    return parks

def generate_mock_campgrounds(park_id: str, n: int) -> List[Campground]:
    campgrounds = []
    for i in range(n):
        campgrounds.append(Campground(
            id=random_id("camp"),
            park_id=park_id,
            name=f"Campground {i+1}",
            description=f"Campground {i+1} in park {park_id}",
            location=random.choice(["North", "South", "East", "West", "Central"]) + " Section",
            elevation_ft=random.randint(500, 8000),
            num_sites=0,  # Will be set after campsites are generated
            amenities=random.sample(CAMP_AMENITIES, random.randint(2, len(CAMP_AMENITIES))),
            season=(random.choice(["April", "May", "June"]), random.choice(["September", "October", "November"]))
        ))
    return campgrounds

def generate_mock_campsites(campground_id: str, n: int) -> List[Campsite]:
    campsites = []
    for i in range(n):
        site_type = random.choice(SITE_TYPES)
        campsites.append(Campsite(
            id=random_id("site"),
            campground_id=campground_id,
            site_number=f"{random.choice(['A', 'B', 'C'])}{i+1}",
            site_type=site_type,
            max_occupancy=random.randint(2, 12) if site_type != "group" else random.randint(10, 30),
            max_vehicles=random.randint(1, 3),
            accessible=random.choice([True, False]),
            power_hookups=random.choice([True, False]),
            water_hookups=random.choice([True, False]),
            sewer_hookups=random.choice([True, False]),
            cost_per_night=round(random.uniform(15, 75), 2)
        ))
    return campsites

def generate_mock_availability(campsite_id: str, days: int) -> List[Availability]:
    today = date.today()
    availabilities = []
    for i in range(days):
        d = today + timedelta(days=i)
        # Simulate realistic booking: 70% available, 20% reserved, 10% unavailable
        roll = random.random()
        if roll < 0.7:
            is_available = True
            is_reserved = False
        elif roll < 0.9:
            is_available = False
            is_reserved = True
        else:
            is_available = False
            is_reserved = False
        availabilities.append(Availability(
            campsite_id=campsite_id,
            date=d,
            is_available=is_available,
            is_reserved=is_reserved
        ))
    return availabilities

def generate_mock_data():
    """
    Generate mock data for parks, campgrounds, campsites, and availability.
    """
    parks = generate_mock_parks(5)
    campgrounds = []
    campsites = []
    availability = []

    for park in parks:
        park_campgrounds = generate_mock_campgrounds(park.id, random.randint(2, 4))
        campgrounds.extend(park_campgrounds)

        for campground in park_campgrounds:
            camp_sites = generate_mock_campsites(campground.id, random.randint(10, 50))
            campground.num_sites = len(camp_sites)
            campsites.extend(camp_sites)

            for site in camp_sites:
                site_availability = generate_mock_availability(site.id, 90)
                availability.extend(site_availability)

    return parks, campgrounds, campsites, availability