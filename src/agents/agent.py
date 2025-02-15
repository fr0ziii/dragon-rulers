import logging
import logging
import json
from src.connectors.http.http_connector import HttpConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Agent:
    """
    A basic trading agent.

    Attributes:
        name (str): The agent's name.
        role (str): The agent's role (e.g., 'analyzer', 'executor').
        strategy (object): The trading strategy the agent uses.
        connector (HttpConnector): The HTTP connector for API interactions.
    """

    def __init__(self, name: str, role: str, strategy, connector: HttpConnector):
        """
        Initializes the Agent with a name, role, strategy, and connector.
        """
        self.name = name
        self.role = role
        self.strategy = strategy
        self.connector = connector
        logging.info("Agent initialized: {} ({})".format(self.name, self.role))

    def process_data(self, data):
        """
        Processes incoming data.
        Placeholder for data processing logic.
        """
        logging.info("Agent {} processing data...".format(self.name))
        pass

    def create_agent(self):
        """Creates the agent via the API."""
        response = self.connector.post("/agents", data={"name": self.name, "role": self.role})
        if response:
            logging.info(f"Agent {self.name} created successfully.")
            return json.loads(response)
        else:
            logging.error(f"Failed to create agent {self.name}.")
            return None

    def get_agent(self, agent_id: int):
        """Retrieves agent information via the API."""
        response = self.connector.get(f"/agents/{agent_id}")
        if response:
            logging.info(f"Retrieved information for agent ID {agent_id}.")
            return json.loads(response)
        else:
            logging.error(f"Failed to retrieve information for agent ID {agent_id}.")
            return None

    def update_agent(self, agent_id: int):
        """Updates agent information via the API."""
        response = self.connector.put(f"/agents/{agent_id}", data={"name": self.name, "role": self.role})
        if response:
            logging.info(f"Updated information for agent ID {agent_id}.")
            return json.loads(response)
        else:
            logging.error(f"Failed to update information for agent ID {agent_id}.")
            return None
    
    def delete_agent(self, agent_id: int):
        """Deletes an agent via the API."""
        response = self.connector.delete(f"/agents/{agent_id}")
        if response:
            logging.info(f"Deleted agent with ID {agent_id}.")
            return json.loads(response)
        else:
            logging.error(f"Failed to delete agent with ID {agent_id}.")
            return None