import env  # noqa: F401 loading dotenv

import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi

from logger import configure_logging
from api.middleware.request_id import RequestIdMiddleware
from api.middleware.log_context import LoggerContextMiddleware
from api.exceptions import validation_exception_handler
from api.routes.register import register_routes
from api.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

configure_logging(logging.DEBUG)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggerContextMiddleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    # Remove all 422 responses
    for path in openapi_schema["paths"].values():
        for method in path.values():
            responses = method.get("responses", {})
            responses.pop("422", None)
            responses["403"] = {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"detail": "Unauthorized"}
                    }
                }
            }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


register_routes(app)
