from fastapi import FastAPI

from .redirects import router as redirects_router
from .webhooks import router as webhooks_router

app = FastAPI(title="WhiteVPN API")

app.include_router(redirects_router)
app.include_router(webhooks_router)
