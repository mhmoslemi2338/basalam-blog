from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_jwt


class jwt_bearer_admin(HTTPBearer):
    user_id=''
    def __init__(self, auto_error: bool = True):
        super(jwt_bearer_admin, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwt_bearer_admin, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            user_id=self.give_user_id(credentials.credentials)
            #tmp=[credentials.credentials]
            #tmp.append(user_id)
            if not self.verify_type(credentials.credentials) :
                raise HTTPException(status_code=403, detail="you have not access.")


            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


    def verify_type(self, jwtoken: str) -> bool:
        payload = decode_jwt(jwtoken)
        if payload["usertype"]=="admin" :
            return True
        else:
            return False





    def give_user_id(self , jwtoken: str):
        tmp=decode_jwt(jwtoken)
        tmp=tmp["user_id"]
        return tmp


    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


        

class jwt_bearer_user(HTTPBearer):
    user_id=''
    def __init__(self, auto_error: bool = True):
        super(jwt_bearer_user, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwt_bearer_user, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            user_id=self.give_user_id(credentials.credentials)
            #tmp=[credentials.credentials]
            #tmp.append(user_id)
            if not self.verify_type(credentials.credentials) :
                raise HTTPException(status_code=403, detail="you have not access.")


            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


    def verify_type(self, jwtoken: str) -> bool:
        payload = decode_jwt(jwtoken)
        if payload["usertype"]=="user" or payload["usertype"]=="admin" :
            return True
        else:
            return False





    def give_user_id(self , jwtoken: str):
        tmp=decode_jwt(jwtoken)
        tmp=tmp["user_id"]
        return tmp


    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


        
