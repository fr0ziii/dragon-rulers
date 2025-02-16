# Algorithmic Trading Bot Framework

## Description

This project aims to develop a flexible and scalable algorithmic trading bot framework for blockchain, leveraging swarm intelligence. It is designed for quantitative traders, software developers, financial analysts, and DeFi enthusiasts. The framework supports multiple blockchain networks, various trading strategies, and provides a user-friendly interface for managing trading bots.

## Getting Started

### Prerequisites

*   Python 3.10 or higher
*   Node.js and npm
*   PostgreSQL and TimeScaleDB (optional for now, will be required later)

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  Create and activate a Python virtual environment:
    ```bash
    python3.10 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Navigate to the `src/ui` directory and install React dependencies:
    ```bash
    cd src/ui
    npm install
    ```

### Running the App

1.  Start the FastAPI backend:
    ```bash
    cd ../..  # Navigate back to the project root
    uvicorn src.api.main:app --reload
    ```

2.  Start the React frontend (in a separate terminal):
    ```bash
    cd src/ui
    npm start
    ```

The React app will be available at `http://localhost:3000`.

## Project Structure

```
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── requirements.txt    # Python dependencies
├── docs/               # Documentation files
├── infrastructure/     # Infrastructure-related files (e.g., Docker, Kubernetes)
├── memory-bank/        # Memory bank for the AI agent
├── scripts/            # Utility scripts
├── src/                # Source code
│   ├── api/            # FastAPI backend
│   │   └── main.py     # FastAPI application
│   ├── agents/         # Trading agents
│   │   └── agent.py    # Base Agent class
│   ├── cli.py          # Command-line interface
│   ├── connectors/     # Connectors to external services (e.g., blockchain, data providers)
│   │   └── http/
│   │       └── http_connector.py # Basic HTTP connector
│   ├── core/           # Core framework components
│   ├── data/           # Data models and database interactions
│   │   ├── data.py     # Data classes
│   │   ├── db.py       # Database connection and setup
│   │   └── schema.sql  # Database schema definition
│   ├── main.py         # Main application entry point (example)
│   ├── strategies/     # Trading strategies
│   │   ├── simple_moving_average.py # Example strategy
│   │   └── strategy.py # Base Strategy class
│   ├── swarms/         # Swarm orchestration logic
│   ├── ui/             # React frontend
│   │   ├── public/
│   │   │   └── index.html
│   │   └── src/
│   │       ├── App.css
│   │       ├── App.js
│   │       ├── index.css
│   │       └── index.js
│   └── utils/          # Utility functions
└── tests/              # Unit and integration tests
    ├── e2e/
    ├── integration/
    └── unit/
        ├── test_agent.py
        ├── test_http_connector.py
        └── test_strategy.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.