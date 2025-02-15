from src.agents.agent import Agent
from src.strategies.simple_moving_average import SimpleMovingAverageStrategy
from src.connectors.http.http_connector import HttpConnector
import datetime
from src.data.data import Data

# --- Instantiate components ---
# 1. Connector
connector = HttpConnector("http://127.0.0.1:8000")  # Use the correct API URL

# 2. Strategy
strategy = SimpleMovingAverageStrategy("SMA_10", "Simple Moving Average (10 periods)", 10)

# 3. Agent
agent = Agent("TraderBot1", "Analyzer", strategy, connector)

# --- Interact with the API ---
# Create the agent
created_agent = agent.create_agent()
print(f"Created agent response: {created_agent}")

# Get agent info
if created_agent:
    retrieved_agent = agent.get_agent(created_agent['id'])
    print(f"Retrieved agent response: {retrieved_agent}")

# Update agent info
if created_agent:
    agent.name = "UpdatedTraderBot1"
    updated_agent = agent.update_agent(created_agent['id'])
    print(f"Updated agent response: {updated_agent}")

# Get agent info again
if created_agent:
    retrieved_agent = agent.get_agent(created_agent['id'])
    print(f"Retrieved agent response after update: {retrieved_agent}")

# Delete agent
if created_agent:
    deleted_agent = agent.delete_agent(created_agent['id'])
    print(f"Deleted agent response: {deleted_agent}")

# Try to get agent info after deletion
if created_agent:
    retrieved_agent = agent.get_agent(created_agent['id'])
    print(f"Retrieved agent response after deletion: {retrieved_agent}")