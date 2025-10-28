from datetime import datetime, timedelta
from app.database import mongo_database_con

async def get_system_stats():
    now = datetime.now(datetime.timezone.utc)
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(weeks=1)
    month_ago = now - timedelta(days=30)
    #DEV: Get de dados referente a coleção users
    user_count = await mongo_database_con["users"].count_documents({})
    active_day = await mongo_database_con["users"].count_documents({"updated_at": {"$gte": day_ago}})
    active_week = await mongo_database_con["users"].count_documents({"updated_at": {"$gte": week_ago}})
    active_month = await mongo_database_con["users"].count_documents({"updated_at": {"$gte": month_ago}})

    #DEV: Implementar função que mostra o status dos sistemas modulares.
    # Exemplo: Conexão com API Gemini e Database
    # system_health = check_all_services()

    #DEV: Implementar coleção changelog com TTL longo e usar aqui para ações recentes
    # recent_activities = [{'type': 'user_created', 'timestamp': now.isoformat(), 'details': 'Sample activity'}]

    return {
        "user_count": user_count,
        "active_users_last_day": active_day,
        "active_users_last_week": active_week,
        "active_users_last_month": active_month
    }

    #DEV: Dados extras para retornar
    # "system_health": system_health,
    # "recent_activities": recent_activities
