

from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId

from app.services.validations import validate_animal_exists
from app.schemas.events import EventCreate
from app.database import mongo_database_con

EVENTS_COLLECTION = mongo_database_con["events"]

async def insert_event(event_dto: EventCreate):
    try:
        animal_exists = await validate_animal_exists(event_dto.animal_id)
        if not animal_exists:
            raise ValueError(f"Animal com ID '{event_dto.animal_id}' não encontrado")
        
        event_dict = event_dto.model_dump(mode='python', exclude_unset=True)
        
        if "event_date" not in event_dict or event_dict["event_date"] is None:
            event_dict["event_date"] = datetime.now(timezone.utc)
        
        create_result = await EVENTS_COLLECTION.insert_one(event_dict)
        return str(create_result.inserted_id)
    
    except ValueError as e:
        print(f"Erro de validação: {e}")
        raise
        
    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        raise

async def find_all_events():
    events = await EVENTS_COLLECTION.find().sort("event_date", -1).to_list(length=100)
    return events

async def find_one_event(event_identifier: str):
    """
    Busca um evento por ID
    Args: event_identifier: ID do evento
    Returns: Documento do evento ou None
    """
    try:
        try:
            event_id = ObjectId(event_identifier)
        except (InvalidId, Exception):
            return None
        
        event = await EVENTS_COLLECTION.find_one({"_id": event_id})
        
        if event:
            event["_id"] = str(event["_id"])
        
        return event
        
    except Exception as e:
        print(f"Erro ao buscar evento: {e}")
        return None