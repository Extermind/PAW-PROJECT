from flask_jwt_extended import JWTManager

jwt = JWTManager()


from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify, request
from .models import Log

def roles_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Sprawdź, czy token jest obecny i prawidłowy
            jwt_data = get_jwt()  # Pobierz dane JWT

            # Sprawdź, czy token zawiera wymagane role
            if 'roles' in jwt_data:
                user_roles = [role['name'] for role in jwt_data['roles']]
                if any(role in required_roles for role in user_roles):
                    response = fn(*args, **kwargs)
                    Log.add_log(jwt_data, request, response)
                    return response
            # Jeśli token nie zawiera wymaganych ról lub jest nieprawidłowy, zwróć odpowiedni komunikat lub status błędu
            return jsonify(message='Insufficient permissions'), 403

        return wrapper

    return decorator