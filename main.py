from typing import List
from fastapi import  FastAPI, Depends, status, Response, HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash
description = ""
app= FastAPI(
    title="Blog",
    description = "Create your blog here"
)
 
models.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags= ['blogs'])
def create(request: schemas.Blog, db: Session= Depends(get_db)): # store the information in database 'db'
    new_blog= models.Blog(title=request.title, body=request.body, creator_id=request.creator_id)
    #new_blog= models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model= List[schemas.ShowBlog], tags= ['blogs'])
def all_blogs(db: Session= Depends(get_db)):
    blogs= db.query(models.Blog).all()
    
    return blogs

#Getting a particular blog with id
@app.get('/blog/{blog_id}', status_code=200, response_model= schemas.ShowBlog, tags= ['blogs'])
def show(blog_id,response: Response,  db: Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {blog_id} is not available')
        
    return blog
    
@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags= ['blogs'])
def delete_blog(blog_id, db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id== blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BLog with id {blog_id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Done'

@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED, tags= ['blogs'])
def update_blog(blog_id:int, request:schemas.Blog, db:Session= Depends(get_db)):
    #import pdb;pdb.set_trace()
    db_blog=db.query(models.Blog).filter(models.Blog.id==blog_id)
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {blog_id} not found")
    # db_blog.update(request)
    db_blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'


 
@app.post('/user', response_model= schemas.ShowUser, tags= ['users'])
def create_user(request: schemas.User, db: Session= Depends(get_db)):
   
    new_user= models.User(name=request.name, email=request.email, description=request.description, password=Hash.bcrypt(request.password))
    #new_user= models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#Show all users
@app.get('/user', response_model= List[schemas.ShowUser], tags= ['users'])
def all_users(db: Session= Depends(get_db)):
    users= db.query(models.User).all()
    return users

#Show a particular user
@app.get('/user/{user_id}', status_code=200, response_model= schemas.ShowUser, tags= ['users'])
def show(user_id,response: Response,  db: Session= Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {user_id} is not available')
        
    return user

#delete user
@app.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags= ['users'])
def delete_user(user_id, db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id== user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id {user_id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return 'Done'