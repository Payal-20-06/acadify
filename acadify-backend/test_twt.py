from src.core.security import (
    create_access_token,
    create_refresh_token,
)


user_id = "test-user-123"

access_token = create_access_token(user_id)
refresh_token = create_refresh_token(user_id)

print("ACCESS TOKEN:")
print(access_token)

print("\nREFRESH TOKEN:")
print(refresh_token)