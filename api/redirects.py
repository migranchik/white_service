from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["redirects"],
)

@router.get("/redirect_dl")
async def redirect_dl(url: str = Query(..., max_length=1024)):
    return RedirectResponse(url=url)
