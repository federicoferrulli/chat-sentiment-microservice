from fastapi import FastAPI, Request
from pydantic import BaseModel
import datetime

class HealthResponse(BaseModel):
    request_id: str
    code: int
    msg: str
    path: str
    status: str
    timestamp: datetime.datetime  


router = FastAPI()

@router.get(
        "/health",
        tags=["Monitoring"],
        summary="Controlla lo stato del servizio",
        status_code=200,
        description="Controlla lo stato del servizio",
        response_description="Il servizio è in esecuzione",
        response_model = HealthResponse
    )
async def ping(req: Request) ->  HealthResponse:
    return {
        "request_id": req.state.request_id,
        "code": 200,
        "msg": "pong!",
        'path': req.url.path,
        'status': 'ok',
        'timestamp': datetime.datetime.now()
    }