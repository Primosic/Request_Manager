# Request Management System

## Overview

The Request Management System is designed to process anonymization requests for Colombian citizens across multiple systems. It provides a centralized API for receiving requests, coordinating verification and processing steps, and monitoring the status of each request.

## Key Features

- **Request Reception**: API endpoints for receiving anonymization requests from authorized systems
- **Verification Process**: Coordination of identity verification across multiple systems
- **Anonymization Execution**: Orchestration of the actual data anonymization process
- **Status Monitoring**: Real-time tracking of request status and progress
- **Administrative Controls**: Administrative endpoints for managing and controlling requests
- **Background Services**: Automatic monitoring and retry services for failed operations
- **Service-Oriented Architecture**: Core functionality organized into dedicated services for better modularity and maintainability

## Project Structure

```
Request_Manager/
u2514u2500u2500 app/                    # Main application directory
    u251cu2500u2500 api/                # API routers and endpoints
    u2502   u251cu2500u2500 admin_router.py     # Administrative endpoints
    u2502   u251cu2500u2500 request_router.py   # Request reception endpoints
    u2502   u251cu2500u2500 status_router.py    # Status query endpoints
    u2502   u2514u2500u2500 verify_router.py    # Verification endpoints
    u251cu2500u2500 core/               # Core business logic
    u2502   u251cu2500u2500 config.py           # Application configuration
    u2502   u251cu2500u2500 notifications.py    # Notification service
    u2502   u2514u2500u2500 process_manager.py  # Legacy process management logic
    u251cu2500u2500 db/                 # Database related files
    u2502   u251cu2500u2500 create_schema.sql   # SQL script for initial schema
    u2502   u2514u2500u2500 database.py         # Database connection setup
    u251cu2500u2500 models/             # Data models
    u2502   u251cu2500u2500 models.py           # SQLAlchemy models
    u2502   u2514u2500u2500 schemas.py          # Pydantic schemas
    u251cu2500u2500 services/           # Services implementing core business logic
    u2502   u251cu2500u2500 anonymization_retry_service.py  # Retry service for anonymization
    u2502   u251cu2500u2500 monitoring_service.py           # Monitoring service
    u2502   u251cu2500u2500 process_service.py              # Process management service
    u2502   u251cu2500u2500 request_service.py              # Request management service
    u2502   u251cu2500u2500 service_factory.py              # Service factory
    u2502   u251cu2500u2500 status_service.py               # Status management service
    u2502   u251cu2500u2500 system_service.py               # System management service
    u2502   u2514u2500u2500 verification_retry_service.py   # Retry service for verification
    u251cu2500u2500 utils/              # Utility functions
    u2502   u2514u2500u2500 helpers.py          # Helper utilities
    u2514u2500u2500 main.py             # Main FastAPI application
u251cu2500u2500 tests/                  # Unit and integration tests
u2502   u251cu2500u2500 api/                    # API endpoint tests
u2502   u251cu2500u2500 core/                   # Core logic tests
u2502   u2514u2500u2500 services/               # Service tests
u251cu2500u2500 .env                    # Environment variables
u251cu2500u2500 functional_test.sh      # Shell script for API functional testing
u251cu2500u2500 init_test_db.py         # Script to initialize test database
u251cu2500u2500 PLANNING.md             # Project planning and architecture
u251cu2500u2500 PRODUCTION_CHECKLIST.md # Production deployment checklist
u251cu2500u2500 pytest.ini              # Pytest configuration
u251cu2500u2500 README.md               # Project documentation
u251cu2500u2500 requirements.txt        # Project dependencies
u251cu2500u2500 server.py               # Main server script for running in various environments
u2514u2500u2500 TASK.md                 # Task tracking
```

## Architecture

The application uses a service-oriented architecture, where core functionalities are separated into dedicated services:

- **RequestService**: Handles creation and management of anonymization requests
- **SystemService**: Manages systems registered for anonymization processing
- **ProcessService**: Controls the process flow between systems and requests
- **StatusService**: Provides status information for requests and processes

This architecture provides better separation of concerns, making the codebase more maintainable and testable.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Microsoft SQL Server
- Microsoft ODBC Driver 17 for SQL Server
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Primosic/Request_Manager.git
   cd Request_Manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables by creating a `.env` file:
   ```
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=1435
   DB_USER=sa
   DB_PASSWORD=your_password
   DB_NAME=db_anon
   DB_SCHEMA=zk_colombia
   
   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   API_DEBUG=True
   
   # Security Configuration
   SECRET_KEY=your-secret-key-for-jwt-tokens
   
   # Monitoring Configurations
   VERIFY_RETRY_INTERVAL=600
   PROCESS_RETRY_INTERVAL=600
   MAX_RETRY_ATTEMPTS=5
   RETRY_BACKOFF_FACTOR=2
   
   # Timeouts (in days)
   DEFAULT_VERIFICATION_TIMEOUT_DAYS=7
   DEFAULT_PROCESSING_TIMEOUT_DAYS=30
   ```

5. Ensure SQL Server is running and accessible with the configured credentials.

6. Initialize the test database (for testing only):
   ```bash
   python init_test_db.py
   ```

## Running the Application

### Development Mode

```bash
# Activate the virtual environment if not already activated
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the application with auto-reload enabled
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Run in production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

The project includes comprehensive unit tests and functional tests.

### Running Unit Tests

```bash
# Run all unit tests
pytest

# Run tests with coverage report
pytest --cov=app tests/

# Run specific test modules
pytest tests/api/test_request_router.py
```

### Running Functional Tests

```bash
# Make sure the application is running first
bash functional_test.sh
```

## Development Guidelines

- Follow PEP8 style guidelines and format with black
- Use type hints for all functions
- Write docstrings for all functions using Google style
- Add appropriate unit tests for new features
- Keep files under 500 lines, refactor if necessary
- Use SQLAlchemy for database operations
- Use Pydantic for data validation

## License

[MIT License](LICENSE)

## Contact

Primosic - GitHub: [Primosic](https://github.com/Primosic)