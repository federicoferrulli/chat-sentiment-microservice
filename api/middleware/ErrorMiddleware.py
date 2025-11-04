from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import traceback
from dotenv import load_dotenv 
from os import environ
from pathlib import Path

current_file_path = Path(__file__)
root_dir = current_file_path.parent.parent
env_path = root_dir / ".env" 
load_dotenv(dotenv_path=env_path)

class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request: Request, call_next):
        """
        Questo middleware cattura qualsiasi eccezione si verifichi
        durante l'elaborazione della richiesta.
        """
    
        env = environ.get("ENVIROMENT")
        try:
            response = await call_next(request)
            return response
        
        except Exception as exc:
            timestamp = datetime.utcnow().isoformat()
            method = request.method
            path = request.url.path
            ip = request.client.host if request.client else "unknown"
            if env == "DEV":
                stack = traceback.format_exc()
            else: 
                stack = "--" 
            
            if isinstance(exc, HTTPException):
                status_code = exc.status_code
                message = exc.detail
            else:
                status_code = 500
                message = str(exc)

            log_message = f"{timestamp} ErrorMiddleware {request.state.request_id}:{method}:{path}:{ip}:{status_code}:{message}"
            print(log_message)

            content = {
                "request_id": request.state.request_id,
                "timestamp": timestamp,
                "status_code": status_code,
                "message": message,
                "path": path,
                "method": method,
                "stack": stack
            }
            
            return JSONResponse(
                status_code=status_code,
                content=content
            )