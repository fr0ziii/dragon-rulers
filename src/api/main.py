from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
from fastapi.middleware.cors import CORSMiddleware
from confluent_kafka import Producer
import json
import os
from dotenv import load_dotenv
from src.data.db import get_db_connection
import psycopg2
from uuid import UUID, uuid4
import bcrypt

load_dotenv()

app = FastAPI()

# --- Kafka Producer Configuration ---
kafka_conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'client.id': 'trading-bot-api'
}
producer = Producer(kafka_conf)

# --- CORS Configuration ---
origins = [
    "http://localhost:3002",  # Frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class Agent(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    strategy_id: UUID
    configuration: Optional[Dict] = None
    status: str

class AgentCreate(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None
    strategy_id: UUID
    configuration: Optional[Dict] = None
    status: str

class User(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: str
    updated_at: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Swarm(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    architecture: str
    configuration: Optional[Dict] = None
    status: str

class SwarmCreate(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None
    architecture: str
    configuration: Optional[Dict] = None
    status: str

class Strategy(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    code: str
    parameters_schema: Optional[Dict] = None

class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    code: str
    parameters_schema: Optional[Dict] = None

# --- Helper Functions ---
def publish_event(topic, event_type, data: dict):
    event = {
        "event_type": event_type,
        "timestamp": str(datetime.datetime.now()),
        "data": data
    }
    producer.produce(topic, json.dumps(event).encode('utf-8'))
    producer.flush()

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Welcome to the Trading Bot API"}


@app.post("/agents", response_model=Agent)
async def create_agent(agent_create: AgentCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO trading_agents (user_id, name, description, strategy_id, configuration, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, user_id, name, description, strategy_id, configuration, status;
            """,
            (agent_create.user_id, agent_create.name, agent_create.description,
             agent_create.strategy_id, json.dumps(agent_create.configuration), agent_create.status)
        )
        agent_data = cur.fetchone()
        db.commit()

    if agent_data:
        agent = Agent(
            id=agent_data[0],
            user_id=agent_data[1],
            name=agent_data[2],
            description=agent_data[3],
            strategy_id=agent_data[4],
            configuration=agent_data[5],
            status=agent_data[6]
        )
        # Publish agent.created event
        publish_event("agents", "agent.created", agent.dict())
        return agent
    else:
        raise HTTPException(status_code=500, detail="Failed to create agent")


@app.get("/agents", response_model=List[Agent])
async def list_agents(db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, user_id, name, description, strategy_id, configuration, status
            FROM trading_agents;
            """
        )
        agents_data = cur.fetchall()

    agents = []
    for agent_data in agents_data:
        agents.append(Agent(
            id=agent_data[0],
            user_id=agent_data[1],
            name=agent_data[2],
            description=agent_data[3],
            strategy_id=agent_data[4],
            configuration=agent_data[5],
            status=agent_data[6]
        ))
    return agents


@app.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, user_id, name, description, strategy_id, configuration, status
            FROM trading_agents
            WHERE id = %s;
            """,
            (str(agent_id),)
        )
        agent_data = cur.fetchone()

    if agent_data:
        return Agent(
            id=agent_data[0],
            user_id=agent_data[1],
            name=agent_data[2],
            description=agent_data[3],
            strategy_id=agent_data[4],
            configuration=agent_data[5],
            status=agent_data[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Agent not found")


@app.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(agent_id: UUID, agent_create: AgentCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            UPDATE trading_agents
            SET user_id = %s, name = %s, description = %s, strategy_id = %s, configuration = %s, status = %s
            WHERE id = %s
            RETURNING id, user_id, name, description, strategy_id, configuration, status;
            """,
            (agent_create.user_id, agent_create.name, agent_create.description,
             agent_create.strategy_id, json.dumps(agent_create.configuration), agent_create.status, str(agent_id))
        )
        agent_data = cur.fetchone()
        db.commit()

    if agent_data:
        agent = Agent(
            id=agent_data[0],
            user_id=agent_data[1],
            name=agent_data[2],
            description=agent_data[3],
            strategy_id=agent_data[4],
            configuration=agent_data[5],
            status=agent_data[6]
        )
        # Publish agent.updated event
        publish_event("agents", "agent.updated", agent.dict())
        return agent
    else:
        raise HTTPException(status_code=404, detail="Agent not found")


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, user_id, name, description, strategy_id, configuration, status
            FROM trading_agents
            WHERE id = %s;
            """, (str(agent_id),)
        )
        agent_data = cur.fetchone()
        if not agent_data:
            raise HTTPException(status_code=404, detail="Agent not found")
        cur.execute("DELETE FROM trading_agents WHERE id = %s;", (str(agent_id),))
        db.commit()

    if agent_data:
        agent = Agent(
                id=agent_data[0],
                user_id=agent_data[1],
                name=agent_data[2],
                description=agent_data[3],
                strategy_id=agent_data[4],
                configuration=agent_data[5],
                status=agent_data[6]
            )
            # Publish agent.deleted event
        publish_event("agents", "agent.deleted", agent.dict())
        return {"message": "Agent deleted"}
    
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/users", response_model=User)
async def create_user(user_create: UserCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        # Hash the password
        hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur.execute(
            """
            INSERT INTO users (id, username, email, password_hash, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            RETURNING id, username, email, created_at, updated_at;
            """,
            (str(uuid4()), user_create.username, user_create.email, hashed_password)
        )
        user_data = cur.fetchone()
        db.commit()

    if user_data:
        return User(
            id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            created_at=str(user_data[3]),
            updated_at=str(user_data[4])
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, username, email, created_at, updated_at
            FROM users
            WHERE id = %s;
            """,
            (str(user_id),)
        )
        user_data = cur.fetchone()

    if user_data:
        return User(
            id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            created_at=str(user_data[3]),
            updated_at=str(user_data[4])
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user_create: UserCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        # Hash the password if it's provided
        if user_create.password:
            hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            set_clause = "username = %s, email = %s, password_hash = %s, updated_at = NOW()"
            values = (user_create.username, user_create.email, hashed_password, str(user_id))
        else:
            set_clause = "username = %s, email = %s, updated_at = NOW()"
            values = (user_create.username, user_create.email, str(user_id))
        
        cur.execute(
            f"""
            UPDATE users
            SET {set_clause}
            WHERE id = %s
            RETURNING id, username, email, created_at, updated_at;
            """,
            values
        )
        user_data = cur.fetchone()
        db.commit()

    if user_data:
        return User(
            id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            created_at=str(user_data[3]),
            updated_at=str(user_data[4])
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s;", (str(user_id),))
        db.commit()
    return {"message": "User deleted"}

@app.post("/swarms", response_model=Swarm)
async def create_swarm(swarm_create: SwarmCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO swarms (id, user_id, name, description, architecture, configuration, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, user_id, name, description, architecture, configuration, status;
            """,
            (str(uuid4()), swarm_create.user_id, swarm_create.name, swarm_create.description,
             swarm_create.architecture, json.dumps(swarm_create.configuration), swarm_create.status)
        )
        swarm_data = cur.fetchone()
        db.commit()

    if swarm_data:
        return Swarm(
            id=swarm_data[0],
            user_id=swarm_data[1],
            name=swarm_data[2],
            description=swarm_data[3],
            architecture=swarm_data[4],
            configuration=swarm_data[5],
            status=swarm_data[6]
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create swarm")

@app.get("/swarms", response_model=List[Swarm])
async def list_swarms(db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, user_id, name, description, architecture, configuration, status
            FROM swarms;
            """
        )
        swarms_data = cur.fetchall()

    swarms = []
    for swarm_data in swarms_data:
        swarms.append(Swarm(
            id=swarm_data[0],
            user_id=swarm_data[1],
            name=swarm_data[2],
            description=swarm_data[3],
            architecture=swarm_data[4],
            configuration=swarm_data[5],
            status=swarm_data[6]
        ))
    return swarms

@app.get("/swarms/{swarm_id}", response_model=Swarm)
async def get_swarm(swarm_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, user_id, name, description, architecture, configuration, status
            FROM swarms
            WHERE id = %s;
            """,
            (str(swarm_id),)
        )
        swarm_data = cur.fetchone()

    if swarm_data:
        return Swarm(
            id=swarm_data[0],
            user_id=swarm_data[1],
            name=swarm_data[2],
            description=swarm_data[3],
            architecture=swarm_data[4],
            configuration=swarm_data[5],
            status=swarm_data[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Swarm not found")

@app.put("/swarms/{swarm_id}", response_model=Swarm)
async def update_swarm(swarm_id: UUID, swarm_create: SwarmCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            UPDATE swarms
            SET user_id = %s, name = %s, description = %s, architecture = %s, configuration = %s, status = %s
            WHERE id = %s
            RETURNING id, user_id, name, description, architecture, configuration, status;
            """,
            (swarm_create.user_id, swarm_create.name, swarm_create.description,
             swarm_create.architecture, json.dumps(swarm_create.configuration), swarm_create.status, str(swarm_id))
        )
        swarm_data = cur.fetchone()
        db.commit()

    if swarm_data:
        return Swarm(
            id=swarm_data[0],
            user_id=swarm_data[1],
            name=swarm_data[2],
            description=swarm_data[3],
            architecture=swarm_data[4],
            configuration=swarm_data[5],
            status=swarm_data[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Swarm not found")

@app.delete("/swarms/{swarm_id}")
async def delete_swarm(swarm_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM swarms WHERE id = %s;", (str(swarm_id),))
        db.commit()
    return {"message": "Swarm deleted"}

@app.post("/strategies", response_model=Strategy)
async def create_strategy(strategy_create: StrategyCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO strategies (id, name, description, code, parameters_schema, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id, name, description, code, parameters_schema;
            """,
            (str(uuid4()), strategy_create.name, strategy_create.description, strategy_create.code,
             json.dumps(strategy_create.parameters_schema))
        )
        strategy_data = cur.fetchone()
        db.commit()

    if strategy_data:
        return Strategy(
            id=strategy_data[0],
            name=strategy_data[1],
            description=strategy_data[2],
            code=strategy_data[3],
            parameters_schema=strategy_data[4]
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create strategy")

@app.get("/strategies", response_model=List[Strategy])
async def list_strategies(db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, name, description, code, parameters_schema
            FROM strategies;
            """
        )
        strategies_data = cur.fetchall()

    strategies = []
    for strategy_data in strategies_data:
        strategies.append(Strategy(
            id=strategy_data[0],
            name=strategy_data[1],
            description=strategy_data[2],
            code=strategy_data[3],
            parameters_schema=strategy_data[4]
        ))
    return strategies

@app.get("/strategies/{strategy_id}", response_model=Strategy)
async def get_strategy(strategy_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, name, description, code, parameters_schema
            FROM strategies
            WHERE id = %s;
            """,
            (str(strategy_id),)
        )
        strategy_data = cur.fetchone()

    if strategy_data:
        return Strategy(
            id=strategy_data[0],
            name=strategy_data[1],
            description=strategy_data[2],
            code=strategy_data[3],
            parameters_schema=strategy_data[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Strategy not found")

@app.put("/strategies/{strategy_id}", response_model=Strategy)
async def update_strategy(strategy_id: UUID, strategy_create: StrategyCreate, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute(
            """
            UPDATE strategies
            SET name = %s, description = %s, code = %s, parameters_schema = %s, updated_at = NOW()
            WHERE id = %s
            RETURNING id, name, description, code, parameters_schema;
            """,
            (strategy_create.name, strategy_create.description, strategy_create.code,
             json.dumps(strategy_create.parameters_schema), str(strategy_id))
        )
        strategy_data = cur.fetchone()
        db.commit()

    if strategy_data:
        return Strategy(
            id=strategy_data[0],
            name=strategy_data[1],
            description=strategy_data[2],
            code=strategy_data[3],
            parameters_schema=strategy_data[4]
        )
    else:
        raise HTTPException(status_code=404, detail="Strategy not found")

@app.delete("/strategies/{strategy_id}")
async def delete_strategy(strategy_id: UUID, db: psycopg2.extensions.connection = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM strategies WHERE id = %s;", (str(strategy_id),))
        db.commit()
    return {"message": "Strategy deleted"}

import datetime
