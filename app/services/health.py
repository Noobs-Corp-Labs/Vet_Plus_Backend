import logging
from app.database import mongo_database_con

logger = logging.getLogger("app")

async def check_system():
    try:
        await mongo_database_con.command("ping")
        return {"status": "ready", "database": "ok"}
    except Exception as excp:
        logger.warning(f"Database readiness check failed: {excp}")
        return {"status": "not ready", "database": str(excp)}