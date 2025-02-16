# Server Guidelines

This document outlines the guidelines and patterns used for building the server-side code in the `src/` directory.

## Framework

The server is built using **FastAPI**, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## API Style

The API follows RESTful principles, with separate endpoints for different resources (agents, users, swarms, strategies).

## Database

The project uses **Supabase** as its database. Interaction with Supabase is done through the Supabase Python client, likely initialized in `src/data/db.py`.

## Data Models

**Pydantic** models are used for:

*   Defining the structure of data sent to and received from the API.
*   Validating request data.
*   Serializing and deserializing data between Python objects and JSON.

Example (from `src/api/models/agent.py`):

```python
class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_id: Optional[UUID] = None
    configuration: Optional[dict] = None
    status: Optional[str] = "active"
```

## Endpoints

API endpoints are organized into controllers, each responsible for a specific resource. For example, `src/api/controllers/agents_controller.py` handles endpoints related to agents.

Endpoints are defined using FastAPI's `APIRouter`. Example (from `agents_controller.py`):

```python
router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

@router.post("", response_model=Agent)
async def create_agent(agent_create: AgentCreate):
    # ... implementation ...
```

## Error Handling

*   `HTTPException` from FastAPI is used to raise HTTP errors (e.g., 404 Not Found, 500 Internal Server Error).
* The code includes try/except blocks to handle potential errors during database operations or other logic.

## Logging

*   The standard Python `logging` module is used for logging.
*   Log levels include `INFO`, `WARNING`, and `ERROR`.
*   Log messages include timestamps, log levels, and descriptive messages.

Example:

```python
logger = logging.getLogger(__name__)
logger.info(f"GET /agents - Listing agents")
```

## Asynchronous Operations

*   The `async` and `await` keywords are used for asynchronous operations, leveraging FastAPI's support for asynchronous request handling.

## Dependency Injection
Although not explicitly shown in the provided files, FastAPI's dependency injection system is likely used for managing dependencies (e.g., database connections, services).

## Event Publishing
The code publishes events (e.g., "agent.created", "agent.updated") to a message queue, likely Kafka, using a `publish_event` function. This suggests an event-driven architecture.

## UUIDs
UUIDs (Universally Unique Identifiers) are used for agent IDs.

## File Structure

The server code is organized into the following directories:

*   `src/`: Root directory for the server code.
    *   `api/`: Contains API-related code.
        *   `controllers/`: Contains API endpoint definitions (routers).
        *   `models/`: Contains Pydantic models for data validation and serialization.
        *   `services/`: Contains business logic and service layer code.
    *   `agents/`: Contains logic related to agents.
    *   `connectors/`: Contains code for interacting with external services (e.g., HTTP, Solana).
    *   `consumers/`: Likely contains message queue consumers.
    *   `core/`: Contains core application logic.
    *   `data/`: Contains database interaction logic and data access objects (DAOs).
    *   `strategies/`: Contains trading strategy implementations.
    *   `swarms/`: Contains logic related to agent swarms.
    *   `utils/`: Contains utility functions.

## Coding Style

*   **Type Hints:** Python type hints are used extensively.
*   **Docstrings:** Docstrings are expected (although not shown in all provided examples).
*   **Naming Conventions:**
    *   Variables and functions: snake_case (e.g., `agent_data`, `create_agent`).
    *   Classes: PascalCase (e.g., `Agent`, `AgentCreate`).
    *   Constants: UPPER_SNAKE_CASE (e.g., `AGENTS_TABLE`).
* **Imports:**
    - Relative imports are used within the `src` directory (e.g., `from src.api.models.agent import Agent`).