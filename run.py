import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=getattr(settings, "server_host", "0.0.0.0"),
        port=int(getattr(settings, "server_port", 8000)),
        reload=True
    )
