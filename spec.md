# parkcamping

## Project Overview
A Python-based MCP (Multi-Channel Protocol) Server that provides information about available camping sites in fictitious national parks. The server will allow users to browse national parks, list campgrounds within those parks, check availability for specific date ranges, and view pricing information.

## Core Functionality
- Browse fictitious national parks
- List campgrounds within a selected park
- Check campsite availability for specific date ranges
- View pricing information for campsites

## Architecture
The application should be built as a Python MCP Server with the following components:
- Core server implementation using a modern Python MCP framework
- RESTful API endpoints for client interactions
- Mock data services that simulate database interactions
- Clean separation between the API layer and the business logic

## Detailed Requirements

### Data Models

#### Park
```python
class Park:
    id: str  # Unique identifier
    name: str  # Park name
    description: str  # Brief description
    location: str  # General location
    established_date: datetime  # When the park was established
    size_acres: int  # Size in acres
    visitor_centers: List[str]  # Names of visitor centers
```

#### Campground
```python
class Campground:
    id: str  # Unique identifier
    park_id: str  # Reference to parent park
    name: str  # Campground name
    description: str  # Brief description
    location: str  # Location within the park
    elevation_ft: int  # Elevation in feet
    num_sites: int  # Total number of campsites
    amenities: List[str]  # Available amenities (restrooms, showers, etc.)
    season: Tuple[str, str]  # Operating season (start_month, end_month)
```

#### Campsite
```python
class Campsite:
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
```

#### Availability
```python
class Availability:
    campsite_id: str  # Reference to campsite
    date: datetime.date  # Specific date
    is_available: bool  # Whether the site is available
    is_reserved: bool  # Whether the site is reserved
```

### API Functions

#### campground_lister
Lists all campgrounds in a specified national park.

```python
def campground_lister(park_id: str) -> List[Campground]:
    """
    List all campgrounds in a specified national park.
    
    Args:
        park_id: Unique identifier for the park
        
    Returns:
        List of Campground objects in the specified park
    """
```

#### availability_by_date
Returns available camping spots for a specified date range.

```python
def availability_by_date(campground_id: str, start_date: datetime.date, nights: int) -> Dict[str, List[datetime.date]]:
    """
    Find available campsites for a specified date range.
    
    Args:
        campground_id: Unique identifier for the campground
        start_date: First night of the stay
        nights: Number of nights to stay
        
    Returns:
        Dictionary mapping campsite_id to a list of available dates
    """
```

#### cost_lister
Lists all campsites in a campground with their associated costs.

```python
def cost_lister(campground_id: str) -> Dict[str, float]:
    """
    List all campsites in a campground with their costs.
    
    Args:
        campground_id: Unique identifier for the campground
        
    Returns:
        Dictionary mapping campsite_id to cost per night (in USD)
    """
```

### Mock Data Generation

The server should include mock data generators for:
1. At least 5 fictitious national parks
2. 2-4 campgrounds per park
3. 10-50 campsites per campground
4. Randomized availability patterns that simulate realistic booking patterns

Example mock data generation function:

```python
def generate_mock_data():
    """
    Generate mock data for parks, campgrounds, campsites, and availability.
    """
    parks = generate_mock_parks(5)
    campgrounds = []
    campsites = []
    availability = []
    
    for park in parks:
        # Generate 2-4 campgrounds per park
        park_campgrounds = generate_mock_campgrounds(park.id, random.randint(2, 4))
        campgrounds.extend(park_campgrounds)
        
        for campground in park_campgrounds:
            # Generate 10-50 campsites per campground
            camp_sites = generate_mock_campsites(campground.id, random.randint(10, 50))
            campsites.extend(camp_sites)
            
            # Generate 90 days of availability data for each campsite
            for site in camp_sites:
                site_availability = generate_mock_availability(site.id, 90)
                availability.extend(site_availability)
    
    return parks, campgrounds, campsites, availability
```

## API Endpoints

The MCP server should expose the following endpoints:

### GET /parks
Returns a list of all national parks.

### GET /parks/{park_id}
Returns detailed information about a specific park.

### GET /parks/{park_id}/campgrounds
Returns a list of all campgrounds in a specific park.

### GET /campgrounds/{campground_id}
Returns detailed information about a specific campground.

### GET /campgrounds/{campground_id}/sites
Returns a list of all campsites in a specific campground.

### GET /campgrounds/{campground_id}/availability
Returns availability for all sites in a campground for a specified date range.

Query parameters:
- start_date: First night of the stay (YYYY-MM-DD)
- nights: Number of nights to stay

### GET /campgrounds/{campground_id}/costs
Returns costs for all sites in a campground.

## Testing Requirements

The server should include comprehensive tests:

1. Unit tests for all core functions
2. Integration tests for API endpoints
3. Load tests to ensure the server can handle multiple concurrent requests

## Non-functional Requirements

1. Performance: API responses should return in under 200ms
2. Scalability: Design should support future expansion to real data sources
3. Documentation: Full API documentation using OpenAPI/Swagger
4. Error handling: Clear error messages with appropriate HTTP status codes

## Implementation Notes

- Use FastAPI for the MCP server implementation
- Store mock data in memory for simplicity
- Include type hints throughout the codebase
- Follow PEP 8 style guidelines
- Implement proper logging
- Use dependency injection for testability

## Future Extensions (Not Required for Initial Implementation)

1. User authentication and authorization
2. Actual database integration (PostgreSQL)
3. Reservation system
4. Weather information integration
5. User reviews and ratings
