import time


import jwt
from decouple import config



JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")




def sign_jwt(user_id: str) :
    payload = {
        "user_id": user_id["email"], 
        "usertype": user_id["usertype"],
        "expires": time.time() + 1200
    }
    token = jwt.encode(payload , JWT_SECRET, algorithm = JWT_ALGORITHM)
    return { "access_token": token}



def decode_jwt(token: str) :
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms = JWT_ALGORITHM)
        #if decoded_token["expires"] >= time.time() : 
        return decoded_token
        #else:
         #   None
    except:
        return {}