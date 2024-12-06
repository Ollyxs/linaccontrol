import uvicorn
from app.core.config import settings

uvicorn.run("app.app:app", host="0.0.0.0", port=settings.PORT)
