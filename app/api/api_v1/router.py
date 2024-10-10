from fastapi import APIRouter
from app.api.api_v1.handlers import linac, tests, test_suite, results
from app.api.auth.jwt import auth_router


router = APIRouter()


router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(linac.linac_router, prefix="/linacs", tags=["linacs"])
router.include_router(tests.test_router, prefix="/tests", tags=["tests"])
router.include_router(
    test_suite.test_suite_router, prefix="/test_suites", tags=["test_suites"]
)
router.include_router(results.results_router, prefix="/results", tags=["results"])
