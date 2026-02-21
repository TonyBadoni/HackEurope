from backend.api import logs, classification, fixer, rules

api_router = APIRouter()

api_router.include_router(logs.router)
api_router.include_router(classification.router)
api_router.include_router(fixer.router)
api_router.include_router(rules.router)
