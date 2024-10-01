## FlyHub - Flight Search Service

This is a FastAPI-based web application that provides flight search functionality. It fetches the cheapest flights between source and destination countries based on user input, leveraging caching with Redis for better performance. The service allows clients to retrieve prices of flights between all possible combinations of top 3 airports in specified countries for a given departure date.

### Features

- Retrieve flight prices based on source country, destination country, and departure date.
- Fetch the top 3 airports from the source and destination countries.
- Automatic caching using Redis to reduce load on the downstream API.
- Support for Docker to run the application in a containerized environment.
- Configurable using environment variables. 

### Technologies Used

- FastAPI
- Pydantic
- Redis (for caching)
- Docker
- Python (>= 3.10)

### Getting Started

#### Prerequisites
Make sure you have the following installed:

- Python 3.10
- Docker
- Docker Compose

### Setup
1. **Clone the repository:**

```bash 
git clone https://github.com/salopadlon/flyhub.git 
cd flyhub
```

2. **Set up environment variables:**

Create a `.env` file in the root directory.

#### Redis Configuration

- **Running Locally**: If you're running Redis locally (outside of Docker), use `redis://localhost:6379` as the `REDIS_URL` in your `.env` file.
- **Running in Docker**: When running the application using Docker Compose, use `redis://redis:6379` as the `REDIS_URL`. This refers to the Redis service name in the Docker Compose network.

3. **(Only for local development) Install dependencies:**

If you're running the app locally (outside of Docker), you need to install the required Python packages 
inside your virtual environment:

```bash
pip install -r requirements.txt
```

### Running the Application

#### Using Docker Compose

1. **Build and run the application with Docker:**
    
```bash
docker-compose up --build
```

This will start the FastAPI app on http://localhost:8000 and Redis for caching.

2. **Access the API documentation:**

Visit the API documentation at http://localhost:8000/docs to test the endpoints.


#### Running Locally

If you are running the application without Docker, make sure you have Redis running and then:

1. **Start the FastAPI server:**

```bash
uvicorn app.main:app --reload
```

2. **Access the API documentation:**

Visit the API documentation at http://localhost:8000/docs to test the endpoints.


### Testing

To run unit tests, use the following command:

```bash
pytest
```

Make sure you have the required dependencies installed before running the tests.

### Linting and Code Formatting

- **Run linters:**

```bash
flake8
```

- **Run formatters:**

```bash
black .
```

- **Run isort:**

```bash
isort .
```

### Caching with Redis

The application uses Redis for caching results to avoid overloading the downstream API. Redis is automatically 
set up using Docker Compose, and the caching behavior is controlled via the `fastapi-cache` package.

### Configuration

All configurations are managed via environment variables defined in the `.env` file. The configuration is handled 
through `load_dotenv` method, which automatically loads these values.

#### Redis Configuration

- **Running Locally**: If you're running Redis locally (outside of Docker), use `redis://localhost:6379` as the `REDIS_URL` in your `.env` file.
- **Running in Docker**: When running the application using Docker Compose, use `redis://redis:6379` as the `REDIS_URL`. This refers to the Redis service name in the Docker Compose network.

### API Endpoints

The application provides the following endpoints:

`GET /api/v1/search-flights`

Search for flights between two countries on a specific date, returning the cheapest flights.

#### Query Parameters:

- `source_country`: The source country ISO code (e.g., `US`).
- `destination_country`: The destination country ISO code (e.g., `IN`).
- `departure_date`: The departure date in `DD-MM-YYYY` format.

#### Response:

The response will contain the cheapest flights between the top 3 airports in the source and destination countries.

Example response:

```json
[
    {
        "src": "JFK",
        "dst": "CDG",
        "price": "300"
    },
    {
        "src": "LAX",
        "dst": "ORY",
        "price": "450"
    }
]
```
