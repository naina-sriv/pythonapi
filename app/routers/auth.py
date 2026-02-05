from .. import models, schema,oauth2,utils
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schema import UserLogin

router=APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_creds: UserLogin, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_creds.email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Invalid credentials")
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
    
    #create a token
    access_token= oauth2.create_access_token(data={"user_id":user.id})
    #return a token
    return {"access_token":access_token, "token_type":"bearer"}
    
    
    
    
    