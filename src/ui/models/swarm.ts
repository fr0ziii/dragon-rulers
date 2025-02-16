export interface Swarm {
  id: string; // Assuming UUID is represented as a string
  user_id: string; // Assuming UUID is represented as a string
  name: string;
  description?: string;
  architecture: string;
  configuration?: Record<string, any>;
  status: string;
}

export interface SwarmCreate {
  user_id: string;
  name: string;
  description?: string;
  architecture: string;
  configuration?: Record<string, any>;
  status: string;
}