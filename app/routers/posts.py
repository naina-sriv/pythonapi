from .. import models, schema
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List 
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(prefix="/posts")

@router.get("/",response_model=List[schema.ResponsePost])
def get_posts(db: Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@router.post("/")
def create_post(post: schema.CreatePost, db: Session = Depends(get_db)):
    #too time taking use dict unpacking instead
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(**post.dict())
    #what it does: 
# So: some_func(**post.dict())
# is exactly the same as writing:
# some_func(
#     title="Sommer",
#     content="why me!",
#     published=False,
#     rating=None
# )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

            
@router.get("/{id}",response_model=schema.ResponsePost) #automatic validation
def get_post(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db)):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # my_posts.pop(find_post_index(id))
    del_post=db.query(models.Post).filter(models.Post.id==id).first()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists.")
    db.delete(del_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.ResponsePost)
def update_posts(id:int,post:schema.UpdatePost, db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    to_update=post_query.first()
    if not to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists.")
    post_query.update(post.dict())
    db.commit()
    return post_query.first()
    