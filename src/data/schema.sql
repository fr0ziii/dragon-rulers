-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- API Keys Table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    api_key VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    revoked BOOLEAN NOT NULL DEFAULT FALSE
);

-- Wallets Table
CREATE TABLE wallets (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    chain VARCHAR(255) NOT NULL,
    address VARCHAR(255) UNIQUE NOT NULL,
    private_key_encrypted TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Trading Agents Table
CREATE TABLE trading_agents (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    strategy_id UUID NOT NULL REFERENCES strategies(id),
    api_key_id UUID REFERENCES api_keys(id),
    configuration JSONB,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Swarms Table
CREATE TABLE swarms (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    architecture VARCHAR(255) NOT NULL,
    configuration JSONB,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Strategies Table
CREATE TABLE strategies (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    parameters_schema JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Blockchains Table
CREATE TABLE blockchains (
    chain_id VARCHAR(255) PRIMARY KEY UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    rpc_url VARCHAR(255) NOT NULL,
    description TEXT
);

-- Market Data Table (TimescaleDB Hypertable)
CREATE TABLE market_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    blockchain VARCHAR(255) NOT NULL REFERENCES blockchains(chain_id),
    dex VARCHAR(255) NOT NULL,
    trading_pair VARCHAR(255) NOT NULL,
    price DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    liquidity DOUBLE PRECISION,
    data_source VARCHAR(255),
    PRIMARY KEY (time, blockchain, dex, trading_pair)
);

-- Convert market_data to a hypertable
SELECT create_hypertable('market_data', 'time', chunk_time_interval => INTERVAL '1 day');

-- Transactions Table
CREATE TABLE transactions (
    signature VARCHAR(255) PRIMARY KEY NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    fee_payer VARCHAR(255),
    status VARCHAR(255),
    log_messages TEXT[]
);

-- Agent Metrics Table
CREATE TABLE agent_metrics (
    agent_id UUID NOT NULL REFERENCES trading_agents(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DOUBLE PRECISION,
    PRIMARY KEY (timestamp, agent_id, metric_name)
);

-- Indexes (as per docs/sd.md)
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_wallets_user_id_chain ON wallets (user_id, chain);
CREATE INDEX idx_trading_agents_user_id_strategy_id ON trading_agents (user_id, strategy_id);
CREATE INDEX idx_strategies_name ON strategies (name);