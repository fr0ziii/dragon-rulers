export interface Agent {
  id: string;
  name: string;
  type: string; // Assuming 'type' is a string, adjust as needed
  configuration: Record<string, any>; // Use a generic object type
  createdAt: Date;
  updatedAt: Date;
}