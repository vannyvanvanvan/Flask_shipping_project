from functools import wraps
from typing import List
from flask import abort
from flask_login import current_user


# Restrict access based on list of ranks
def rank_required(ranks:List[str]):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # Only allow access if user has required rank
            if current_user.rank in ranks:
              func(*args, **kwargs)
            else:
              return abort(403)  # Forbidden
        return decorated_view
    return decorator