import logging
import os

import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    os.environ.update({
        "NLS_LANG": "RUSSIAN_RUSSIA.UTF8",
        "PROJECT_ROOT": os.path.dirname(os.path.abspath(__file__))
    })
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level=getattr(logging, settings.LOG_LEVEL.upper()),
        reload=True,
        loop="uvloop",
        access_log=False,
    )
