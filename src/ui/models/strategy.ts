export interface Strategy {
  id: string; // Assuming UUID is represented as a string
  name: string;
  description?: string;
  code: string;
  parameters_schema?: Record<string, any>; // Generic object type
}

export interface StrategyCreate {
  name: string;
  description?: string;
  code: string;
  parameters_schema?: Record<string, any>;
}