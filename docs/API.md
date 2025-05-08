# ParkCamping MCP Server API Documentation

This document describes the RESTful API endpoints provided by the ParkCamping MCP server.

## Base URL

```
http://localhost:8000/
```

## Endpoints

### GET /parks

Returns a list of all national parks.

**Response:**  
`200 OK`  
```json
[
  {
    "id": "park_XXXXXX",
    "name": "Redwood Valley National Park",
    "description": "...",
    "location": "...",
    "established_date": "1965-05-12T00:00:00",
    "size_acres": 123456,
    "visitor_centers": ["Visitor Center 1", "Visitor Center 2"]
  },
  ...
]
```

---

### GET /parks/{park_id}

Returns detailed information about a specific park.

**Response:**  
`200 OK`  
See above for Park object.

---

### GET /parks/{park_id}/campgrounds

Returns a list of all campgrounds in a specific park.

**Response:**  
`200 OK`  
```json
[
  {
    "id": "camp_XXXXXX",
    "park_id": "park_XXXXXX",
    "name": "Campground 1",
    "description": "...",
    "location": "...",
    "elevation_ft": 1234,
    "num_sites": 20,
    "amenities": ["restrooms", "showers"],
    "season": ["May", "October"]
  },
  ...
]
```

---

### GET /campgrounds/{campground_id}

Returns detailed information about a specific campground.

**Response:**  
`200 OK`  
See above for Campground object.

---

### GET /campgrounds/{campground_id}/sites

Returns a list of all campsites in a specific campground.

**Response:**  
`200 OK`  
```json
[
  {
    "id": "site_XXXXXX",
    "campground_id": "camp_XXXXXX",
    "site_number": "A1",
    "site_type": "tent",
    "max_occupancy": 6,
    "max_vehicles": 2,
    "accessible": false,
    "power_hookups": true,
    "water_hookups": false,
    "sewer_hookups": false,
    "cost_per_night": 35.0
  },
  ...
]
```

---

### GET /campgrounds/{campground_id}/availability

Returns availability for all sites in a campground for a specified date range.

**Query Parameters:**
- `start_date` (YYYY-MM-DD): First night of the stay
- `nights` (int): Number of nights to stay

**Response:**  
`200 OK`  
```json
{
  "site_XXXXXX": ["2025-07-01", "2025-07-02"],
  ...
}
```

---

### GET /campgrounds/{campground_id}/costs

Returns costs for all sites in a campground.

**Response:**  
`200 OK`  
```json
{
  "site_XXXXXX": 35.0,
  ...
}
```

---

## Error Responses

- `404 Not Found`: Resource does not exist
- `400 Bad Request`: Invalid parameters

---

## OpenAPI/Swagger

Interactive API docs are available at `/docs` when the server is running.