# ParkCamping MCP Server

A Python-based MCP (Multi-Channel Protocol) server that provides information about available camping sites in fictitious national parks. The server allows users to browse national parks, list campgrounds, check campsite availability, and view pricing information.

## Features

- Browse fictitious national parks
- List campgrounds within a selected park
- Check campsite availability for specific date ranges
- View pricing information for campsites
- RESTful API with OpenAPI/Swagger docs
- In-memory mock data (no database required)
- Fully type-annotated, PEP8-compliant code
- Unit and integration tests

## Requirements

- Python 3.12 (preferred) or 3.11
- pip

## Setup

1. **Clone the repository**  
   ```sh
   git clone <your-repo-url>
   cd park_camping
   ```

2. **Create a virtual environment**  
   ```sh
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

## Running the Server

```sh
uvicorn app.main:app --reload
```

- The API will be available at [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running Tests

- **Unit and integration tests:**  
  ```sh
  pytest
  ```

## Code Quality

- **Lint:**  
  ```sh
  flake8 app/
  ```
- **Format:**  
  ```sh
  black app/ tests/
  ```

## API Documentation

See [`docs/API.md`](docs/API.md:1) for endpoint details and example requests.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md:1) for release history.

## License

MIT License