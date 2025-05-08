from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from datetime import date
import logging

from app.models import Park, Campground, Campsite, Availability
from app.services import DataService

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("parkcamping")

app = FastAPI(
    title="ParkCamping MCP Server",
    description="API for browsing national parks, campgrounds, campsites, and availability.",
    version="1.0.0"
)

# Allow CORS for all origins (for demo/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_data_service():
    # Singleton pattern for in-memory data
    if not hasattr(get_data_service, "instance"):
        get_data_service.instance = DataService()
    return get_data_service.instance

@app.get("/parks", response_model=List[Park])
def list_parks(service: DataService = Depends(get_data_service)):
    """Returns a list of all national parks."""
    return service.parks

@app.get("/parks/{park_id}", response_model=Park)
def get_park(park_id: str, service: DataService = Depends(get_data_service)):
    """Returns detailed information about a specific park."""
    park = service.park_index.get(park_id)
    if not park:
        logger.warning(f"Park not found: {park_id}")
        raise HTTPException(status_code=404, detail="Park not found")
    return park

@app.get("/parks/{park_id}/campgrounds", response_model=List[Campground])
def list_campgrounds(park_id: str, service: DataService = Depends(get_data_service)):
    """Returns a list of all campgrounds in a specific park."""
    campgrounds = service.campground_lister(park_id)
    if not campgrounds:
        logger.warning(f"No campgrounds found for park: {park_id}")
        raise HTTPException(status_code=404, detail="No campgrounds found for this park")
    return campgrounds

@app.get("/campgrounds/{campground_id}", response_model=Campground)
def get_campground(campground_id: str, service: DataService = Depends(get_data_service)):
    """Returns detailed information about a specific campground."""
    campground = service.campground_index.get(campground_id)
    if not campground:
        logger.warning(f"Campground not found: {campground_id}")
        raise HTTPException(status_code=404, detail="Campground not found")
    return campground

@app.get("/campgrounds/{campground_id}/sites", response_model=List[Campsite])
def list_campsites(campground_id: str, service: DataService = Depends(get_data_service)):
    """Returns a list of all campsites in a specific campground."""
    sites = service.campground_sites.get(campground_id, [])
    if not sites:
        logger.warning(f"No campsites found for campground: {campground_id}")
        raise HTTPException(status_code=404, detail="No campsites found for this campground")
    return sites

@app.get("/campgrounds/{campground_id}/availability", response_model=Dict[str, List[date]])
def get_availability(
    campground_id: str,
    start_date: date = Query(..., description="First night of the stay (YYYY-MM-DD)"),
    nights: int = Query(..., gt=0, le=30, description="Number of nights to stay"),
    service: DataService = Depends(get_data_service)
):
    """Returns availability for all sites in a campground for a specified date range."""
    try:
        result = service.availability_by_date(campground_id, start_date, nights)
        if not result:
            logger.info(f"No availability found for campground {campground_id} on {start_date} for {nights} nights")
            return JSONResponse(status_code=200, content={})
        return result
    except Exception as e:
        logger.error(f"Error in availability lookup: {e}")
        raise HTTPException(status_code=400, detail="Invalid request parameters")

@app.get("/campgrounds/{campground_id}/costs", response_model=Dict[str, float])
def get_costs(campground_id: str, service: DataService = Depends(get_data_service)):
    """Returns costs for all sites in a campground."""
    costs = service.cost_lister(campground_id)
    if not costs:
        logger.warning(f"No costs found for campground: {campground_id}")
        raise HTTPException(status_code=404, detail="No costs found for this campground")
    return costs