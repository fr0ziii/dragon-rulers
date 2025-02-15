-- Create the 'agents' table
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'strategies' table
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'agent_strategies' linking table
CREATE TABLE agent_strategies (
    agent_id INTEGER REFERENCES agents(id),
    strategy_id INTEGER REFERENCES strategies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (agent_id, strategy_id)
);

-- Create the 'trades' table (for TimeScaleDB)
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(id),
    symbol VARCHAR(255) NOT NULL,
    quantity NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Convert 'trades' table to a hypertable (TimeScaleDB specific)
SELECT create_hypertable('trades', 'timestamp');