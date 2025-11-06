from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status

from app.crud.events import find_all_events, find_by_animal_identifier, find_one_event, insert_event
from app.schemas.events import EventCreate, EventResponse
from app.schemas.communs import ListResponse

router = APIRouter()

@router.post("/", 
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(body: EventCreate):
    try:
        event_id = await insert_event(body)
        created_event = await find_one_event(event_id)
        
        if not created_event:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Erro ao recuperar evento criado."
            )
        
        return created_event
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao criar evento."
        )

@router.get("/", 
    response_model=ListResponse[EventResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_events():
    try:
        events = await find_all_events()
        for event in events:
            event["_id"] = str(event["_id"])
            # if event.get("breed") and "_id" in event["breed"]: # DEV: Setar de acordo com response de aniamals, se tiver;
            #     event["breed"]["_id"] = str(event["breed"]["_id"])

        return ListResponse(
            count=len(events),
            rows=events
        )
    
    except Exception as e:
        print(f"Erro ao buscar eventos recentes: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar a lista de eventos."
        )
    
@router.get("/{event_identifier}", 
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
)
async def get_event_by_id(
    event_identifier: Annotated[
        str,
        Path(
            description="Id of the event to retrieve",
            example="String"
        )
    ]
):
    try:
        event = await find_one_event(event_identifier)
        if event is None:
            raise HTTPException(status_code=404, detail='Event not found')
        return event
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar eventos recentes: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar a lista de eventos."
        )


@router.get("/animal/{animal_identifier}", 
    response_model=ListResponse[EventResponse],
    status_code=status.HTTP_200_OK,
)
async def get_events_by_animal_identifier(
    animal_identifier: Annotated[
        str,
        Path(
            description="Id of the animal to retrieve events",
            example="String"
        )
    ]
):
    try:
        events = await find_by_animal_identifier(animal_identifier)
        for event in events:
            event["_id"] = str(event["_id"])

        return ListResponse(
            count=len(events),
            rows=events
        )
    
    except Exception as e:
        print(f"Erro ao buscar eventos recentes: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao buscar a lista de eventos."
        )