import os
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from supabase import create_client
from supabase.lib.client_options import ClientOptions

client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
    options=ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
    ),
)


def get_auth_user_id(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> UUID:
    try:
        token = authorization.credentials
        id = jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=["HS256"],
            audience="authenticated",
            issuer=f"{os.environ.get("SUPABASE_URL")}/auth/v1",
        ).get("sub")
        user = client.auth.admin.get_user_by_id(id)
        if user is None:
            raise Exception("User not found")
        auth_user_id = UUID(id)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return auth_user_id
