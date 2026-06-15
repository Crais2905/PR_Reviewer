from  fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user import UserService
from app.db.session import get_session
from app.auth.tokens import decode_token
from app.schemas.user import UserPublic


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
):
    try:
        token = request.cookies.get("access_token")
        payload = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_service.get_user(email, session)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
