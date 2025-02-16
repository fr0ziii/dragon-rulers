from fastapi import FastAPI
from src.api.controllers import agents_controller, users_controller, swarms_controller, strategies_controller
from src.api.services.common import setup_cors
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# --- CORS Configuration ---
setup_cors(app)

# --- API Endpoints ---
@app.get("/")
async def root():
    logger.info("GET / - Root endpoint accessed")
    return {"message": "Welcome to the Trading Bot API"}

app.include_router(agents_controller.router)
app.include_router(users_controller.router)
app.include_router(swarms_controller.router)
app.include_router(strategies_controller.router)
