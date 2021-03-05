from fastapi import FastAPI , HTTPException , Body , Depends

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.my_model import *
from app.auth_handler import sign_jwt
from app.auth_bearer import jwt_bearer_admin , jwt_bearer_user
from app.psqlDB import *
import psycopg2
import redis
import hashlib


redis_host = "localhost"
redis_port = 6379
redis_password = ""

connect_R = redis.StrictRedis(host = redis_host, port = redis_port, password = redis_password, decode_responses = True)


create_TABLE()
app = FastAPI(title = "BAtwitter")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')




@app.get("/", tags = ['root'])
async def Home_page():
    return {"message" : " welcome to BAtwitter"}



@app.get("/posts" , tags = ["posts"])
async def read_all_posts():
    tmp_posts = all_DB()
    return {"posts": tmp_posts}


@app.post("/posts",  dependencies = [Depends(jwt_bearer_admin())], tags = ["posts"], 
                 response_model = postschema_response , response_model_include = {"title", "body" })
async def add_post(post : postschema_response):
    
    #user=jwt_bearer().give_user_id(jwt_bearer().)
    tmp = dict(post) 
    tmp["likes"]=0
    tmp["comment"]=[]
    add_post_psql(tmp)
    return post


  

@app.get("/posts/{id}" , tags = ["posts"])
async def read_single_posts(id : int):
    post=get_single_post(id)
    if post!=[]:
        return {"posts": post}
    else:
        raise HTTPException(status_code = 404 , detail = " post not found")




@app.put("/posts/{id}",dependencies = [Depends(jwt_bearer_user())], tags = ["posts"])
async def like_post(id: int):
    if DB_like_post(id)==1:
        return {"message": " the post with given id successfully liked "}

    raise HTTPException(status_code = 404 , detail = " post not found")



@app.put("/posts/{id}/comment/",dependencies = [Depends(jwt_bearer_user())], tags = ["posts"])
async def comment_post(comment : comment_post):
    comment=dict(comment)
    if DB_comment_post(comment)==1:
        return {"message":  " the comment with given id successfully added " }

    raise HTTPException(status_code = 404 , detail = " post not found")












def add_user(client):
    name = client["name"]
    username = client["email"]
    password = client["password"]
    usertype =client["usertype"]

    hs = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if  not connect_R.hexists(username, "name"):
        try:   
            connect_R.hmset(username, {"name":name, "password":hs , "usertype" :usertype })
            return True
        except Exception as e:
            return e    
    return False
    

@app.post("/user/signup", tags = ["user"])
async def user_sign_up(user: my_user = Body(...)):
    #users.append(user) # replace with db call, making sure to hash the password first
    if add_user(dict(user)) :
        return sign_jwt(dict(user))
    raise HTTPException(status_code = 406, detail = "username is already used")
    


def user_check( client : userLogin):
    username = client.email
    password = client.password
    if connect_R.hget(username, "password") == None:
        raise HTTPException(status_code = 403, detail = "Invalid username or password.")
    else:
        master_pass = connect_R.hget(username, "password")
        hs = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if hs == master_pass :
            return 1
        else:
            return 0
        


@app.post("/user/login" , tags = ["user"])
async def user_sign_in( client : userLogin = Body (...)):
    if user_check(client) : 
        return sign_jwt(client.email)
    else: 
        return { "Error" : " email or password is not correct."}



