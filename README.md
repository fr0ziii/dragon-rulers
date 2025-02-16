# Dragon Rulers  🐉🤖📈

<div align="center">
  <img src="cover.jpeg" alt="Dragon Rulers Banner" width="100%"/>
</div>

## Description

Dragon Rulers is a flexible and scalable algorithmic trading bot framework for blockchain, leveraging swarm intelligence. It is designed for:

*   **Quantitative Traders:** Develop and deploy sophisticated trading strategies.
*   **Software Developers:** Extend the framework with custom integrations and features.
*   **Financial Analysts:** Analyze market data and backtest trading strategies.
*   **DeFi Enthusiasts:** Explore and participate in the decentralized finance ecosystem.

**Key Features:**

*   **Multi-Blockchain Support:** Connect to various blockchain networks (e.g., Solana, NEAR, Binance Smart Chain, Polygon - planned).
*   **Diverse Trading Strategies:** Implement custom strategies or use pre-built options (e.g., simple moving average, machine learning-based - planned).
*   **Swarm Intelligence:** Utilize collective decision-making of multiple trading agents (planned).
*   **User-Friendly Interface:** Manage bots and monitor performance through a React-based UI.
*   **Event-Driven Architecture:** Uses Kafka for asynchronous communication and scalability.
*   **Extensible Design:** Easily add new features, strategies, and blockchain integrations.

**Benefits:**

*   **Automation:** Automate trading activities and reduce manual intervention.
*   **Scalability:** Scale trading operations by deploying multiple bots and swarms.
*   **Flexibility:** Adapt to changing market conditions with dynamic strategies.
*   **Data-Driven Decisions:** Leverage real-time market data and analysis.
*   **Community-Driven:** Open-source project with contributions from the community.

---

## Getting Started

### Prerequisites

*   **Python 3.10 or higher**
*   **Node.js and npm**
*   **Supabase Account:** Create a free account at [supabase.com](https://supabase.com).
*   **Kafka:** Required for the event-driven architecture. You'll need a Kafka broker running. (Instructions for setting up Kafka are not yet included in this README, but will be added later.)

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

4.  **Navigate to the `src/ui` directory and install NextJS dependencies:**

    ```bash
    cd src/ui
    npm install
    ```

5.  **Set up Supabase:** Follow the initial steps in the Supabase "Get Started" guide to create a new project: [https://supabase.com/docs/guides/getting-started](https://supabase.com/docs/guides/getting-started).  After creating the project, link it to this repository by following Supabase's instructions for linking to an existing project.

6.  **Environment Variables:**
    *   Create a `.env` file in the root directory of the project by copying the provided `.env.example` file:

        ```bash
        cp .env.example .env
        ```

    *   Fill in the necessary environment variables in the `.env` file.  This includes your Supabase project credentials (URL and Anon Key) and your Kafka broker address (e.g., `KAFKA_BOOTSTRAP_SERVERS=localhost:9092`).

### Running the App

1.  **Start the FastAPI backend:**

    ```bash
    cd ../..  # Navigate back to the project root
    uvicorn src.api.main:app --reload --port 8000
    ```

2.  **Start the React frontend (in a separate terminal):**

    ```bash
    cd src/ui
    npm run dev
    ```

The React app will be available at `http://localhost:3000`.

---

## Project Structure

```
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── requirements.txt    # Python dependencies
├── infrastructure/     # Infrastructure-related files (e.g., Docker, Kubernetes)
├── scripts/            # Utility scripts
├── src/                # Source code
│   ├── api/            # FastAPI backend
│   │   └── main.py     # FastAPI application with API endpoints for users, agents, swarms, and strategies
│   ├── agents/         # Trading agents
│   │   └── agent.py    # Base Agent class
│   ├── cli.py          # Command-line interface
│   ├── connectors/     # Connectors to external services (e.g., blockchain, data providers)
│   │   └── http/
│   │       └── http_connector.py # Basic HTTP connector
│   ├── consumers/      # Event consumers
│   │   └── agent_consumer.py  # Consumes agent-related events from Kafka
│   ├── core/           # Core framework components
│   ├── data/           # Data models and database interactions
│   │   ├── data.py     # Data classes
│   │   ├── db.py       # Database connection and setup
│   │   ├── schema.sql  # Database schema definition
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

### Event-Driven Architecture

*   Expand the event consumer to handle other events (e.g., `agent.updated`, `agent.deleted`).
*   Integrate the event consumer with the database to store agent data.

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
*   Fully integrate Shadcn UI.
*   Implement actual dashboard functionality.

### Testing and Deployment

*   Implement more robust error handling.
*   Add logging to more components.
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