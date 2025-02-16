// src/ui/src/lib/api.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getAgents() {
  const response = await fetch(`${API_BASE_URL}/agents`);
  if (!response.ok) {
    throw new Error(`Failed to fetch agents: ${response.statusText}`);
  }
  return response.json();
}

// Add other API functions as needed (e.g., getAgentById, createAgent, etc.)