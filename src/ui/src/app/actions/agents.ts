// src/app/actions/agents.ts
'use server';

import { Agent } from '@/models/agent';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getAgents() {
  try {
    const response = await fetch(`${API_BASE_URL}/agents`);
    if (!response.ok) {
      throw new Error(`Failed to fetch agents: ${response.statusText}`);
    }
    return await response.json();
  } catch (error: any) {
    return { error: error.message };
  }
}

// Add other agent-related actions here (createAgent, updateAgent, etc.)