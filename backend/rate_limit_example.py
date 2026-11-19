# Example rate-limit middleware (optional, add to app.py if desired)
# Requires: pip install slowapi

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Then decorate:
# @app.post("/api/login")
# @limiter.limit("5/minute")
# def login(...):
#     ...
