import uvicorn
import router
from config.settings import config

from fastapi import FastAPI

app = FastAPI()
router.init(app)

if __name__ == '__main__':
    uvicorn.run(
        'apps.site.app:app',
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL,
        reload=True
    )