from .. import models, schema
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router=APIRouter(tags="Authentication")

@router.post("\login")
def login(db:Session=Depends(get_db)):
    
    
    
    