-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- API Keys Table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    api_key TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    revoked BOOLEAN NOT NULL DEFAULT FALSE
);

-- Wallets Table
CREATE TABLE wallets (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    chain TEXT NOT NULL,
    address TEXT UNIQUE NOT NULL,
    private_key_encrypted TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Strategies Table
CREATE TABLE strategies (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    parameters_schema JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Trading Agents Table
CREATE TABLE trading_agents (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    description TEXT,
    strategy_id UUID NOT NULL REFERENCES strategies(id),
    api_key_id UUID REFERENCES api_keys(id),
    configuration JSONB,
    status TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Swarms Table
CREATE TABLE swarms (
    id UUID PRIMARY KEY UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    description TEXT,
    architecture TEXT NOT NULL,
    configuration JSONB,
    status TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Blockchains Table
CREATE TABLE blockchains (
    chain_id TEXT PRIMARY KEY UNIQUE NOT NULL,
    name TEXT NOT NULL,
    rpc_url TEXT NOT NULL,
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
    signature TEXT PRIMARY KEY NOT NULL,
    blockchain TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    fee_payer TEXT,
    status TEXT,
    log_messages TEXT[]
);

-- Agent Metrics Table
CREATE TABLE agent_metrics (
    agent_id UUID NOT NULL REFERENCES trading_agents(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value DOUBLE PRECISION,
    PRIMARY KEY (timestamp, agent_id, metric_name)
);

-- Indexes (as per docs/sd.md)
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_wallets_user_id_chain ON wallets (user_id, chain);
CREATE INDEX idx_trading_agents_user_id_strategy_id ON trading_agents (user_id, strategy_id);
CREATE INDEX idx_strategies_name ON strategies (name);