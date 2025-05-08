import pytest
from datetime import date, timedelta
from app.services import DataService

@pytest.fixture(scope="module")
def service():
    return DataService()

def test_campground_lister(service):
    # Pick a park with campgrounds
    park = service.parks[0]
    campgrounds = service.campground_lister(park.id)
    assert isinstance(campgrounds, list)
    assert all(c.park_id == park.id for c in campgrounds)
    assert len(campgrounds) >= 2

def test_availability_by_date(service):
    # Pick a campground and a date range
    campground = service.campgrounds[0]
    start = date.today() + timedelta(days=1)
    nights = 3
    result = service.availability_by_date(campground.id, start, nights)
    assert isinstance(result, dict)
    # At least one site should have some availability
    assert any(len(dates) > 0 for dates in result.values())

def test_cost_lister(service):
    campground = service.campgrounds[0]
    costs = service.cost_lister(campground.id)
    assert isinstance(costs, dict)
    assert all(isinstance(v, float) for v in costs.values())
    assert len(costs) == campground.num_sites