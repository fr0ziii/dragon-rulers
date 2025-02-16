# Algorithmic Trading Bot Framework

## Description

This project aims to develop a flexible and scalable algorithmic trading bot framework for blockchain, leveraging swarm intelligence. It is designed for quantitative traders, software developers, financial analysts, and DeFi enthusiasts. The framework supports multiple blockchain networks, various trading strategies, and provides a user-friendly interface for managing trading bots.

---

## Getting Started

### Prerequisites

*   **Python 3.10 or higher**
*   **Node.js and npm**
*   **Supabase Account:** Create a free account at [supabase.com](https://supabase.com).

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/fr0ziii/dragon-rulers
    cd dragon-rulers
    ```

2.  **Create and activate a Python virtual environment:**

    ```bash
    python3.10 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Navigate to the `src/ui` directory and install React dependencies:**

    ```bash
    cd src/ui
    npm install
    ```

5.  **Set up Supabase:** Follow the instructions in [`docs/supabase_setup.md`](docs/supabase_setup.md) to set up your Supabase project and link it to this repository.

### Running the App

1.  **Start the FastAPI backend:**

    ```bash
    cd ../..  # Navigate back to the project root
    uvicorn src.api.main:app --reload
    ```

2.  **Start the React frontend (in a separate terminal):**

    ```bash
    cd src/ui
    npm start
    ```

The React app will be available at `http://localhost:3000`.

---

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

---

## Roadmap

The following features and improvements are planned for future development:

### Database Integration

*   Complete the Supabase integration, including connecting the application to the database.
*   Set up Alembic for database migrations.

### Enhanced Agent Capabilities

*   Implement more sophisticated trading strategies (e.g., machine learning-based strategies, arbitrage strategies).
*   Add support for different order types (e.g., limit orders, stop-loss orders).
*   Implement risk management features (e.g., position sizing, stop-loss).

### Swarm Intelligence

*   Implement various swarm architectures (e.g., majority voting, weighted averaging, hierarchical swarms).
*   Develop communication protocols for agents within a swarm.
*   Implement mechanisms for swarm adaptation and learning.

### Blockchain Integration

*   Integrate with multiple blockchain networks (e.g., Solana, NEAR, Binance Smart Chain, Polygon).
*   Support interaction with various decentralized exchanges (DEXs).
*   Implement on-chain data retrieval and analysis.

### Data Integration

*   Integrate with real-time market data providers (e.g., Pyth Network, Jupiter Aggregator).
*   Implement data pipelines for processing and storing market data.
*   Incorporate sentiment analysis from social media and news sources.

### User Interface

*   Improve the user interface for agent and swarm management.
*   Add real-time monitoring of agent and swarm performance.
*   Implement comprehensive reporting and analytics.

### Testing and Deployment

*   Implement thorough unit and integration tests.
*   Develop backtesting and paper trading capabilities.
*   Create deployment scripts and documentation for various cloud platforms.

### Security

*   Implement robust security measures, including key management, multi-factor authentication, and role-based access control.

### Extensibility

*   Design the framework to be easily extensible with new features, strategies, and blockchain integrations.

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.