from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.models.machine import Machine
from app.models.telemetry import Telemetry
from app.mqtt.client import create_mqtt_client
from app.api.telemetry import router as telemetry_router
from app.api.analytics import router as analytics_router
from app.api.ml import router as ml_router


logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Create and start MQTT client
    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()

    app.state.mqtt_client = mqtt_client

    logger.info("UrjaIQ backend started")
    logger.info("MQTT ingestion started")

    try:
        yield

    finally:
        logger.info("Shutting down MQTT ingestion")

        mqtt_client.loop_stop()
        mqtt_client.disconnect()

        logger.info("UrjaIQ backend stopped")


app = FastAPI(
    title="UrjaIQ API",
    description="Industrial Energy & Process Optimization Platform",
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telemetry_router)
app.include_router(analytics_router)
app.include_router(ml_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to UrjaIQ API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "urjaiq-backend",
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect():
            return {
                "status": "healthy",
                "database": "connected",
            }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error),
        }