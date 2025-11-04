from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from datetime import datetime


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        timestamp = datetime.utcnow().isoformat()
        method = request.method
        path = request.url.path
        ip = request.client.host if request.client else "unknown"
        log_message = f"{timestamp} LoggerMiddleware {request_id}:{method}:{path}:{ip}"
        print(log_message)
        return await call_next(request)