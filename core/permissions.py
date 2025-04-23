from typing import List

from fastapi import Depends, HTTPException, status

from core.security import get_current_user
from user.models import UserRole
from user.schemas import UserDB


def role_required(allowed_user_roles: List[UserRole]):
    
    def wrapper(
        current_user: UserDB = Depends(get_current_user)
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized User"
            )
        
        if current_user.user_role not in allowed_user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. only, {[role.value for role in                  allowed_user_roles]} can perform this action"
            )
        
        return current_user

    return wrapper
        