from fastapi import APIRouter
from app.services.workflow_service import (
    get_machine_status,
    get_order_status
)

router = APIRouter(prefix="/workflow", tags=["workflow"])

@router.get("/machine/{machine_id}")
def machine_status(machine_id: str):
    data = get_machine_status(machine_id)
    return {"machine_id": machine_id, "status": data}

@router.get("/order/{order_id}")
def order_status(order_id: str):
    data = get_order_status(order_id)
    return {"order_id": order_id, "status": data}

@router.get("/safety")
def safety_alerts():
    # you can expand with real logic or mock data
    alerts = [
        {"id": 1, "alert": "Oil spill near line 3"},
        {"id": 2, "alert": "Machine B7 overheating"},
    ]
    return {"alerts": alerts}
