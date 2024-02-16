from .. import models, schemas
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Response, APIRouter
from ..database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # the query object is performing the sql
    posts = db.query(models.Post).all()
    # FastAPI uses the jsonable_encoder function internally to serialize Python objects into JSON.
    return posts


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # x = find_post(id)
    # if x is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'Post with id:{id} not found')
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'msg':f'Post with id:{id} not found'}
    # else:
    #     response.status_code = status.HTTP_200_OK
    #     return {'data': x}
    # cursor.execute("""select * from posts where id=%s""", (str(id)),)
    # post = cursor.fetchone()
    post = db.query(models.Post).filter_by(id=id).first()
    db.query(models.Post).filter
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# the parameter will convert the body into dict format and assign it to the variable payload
# def create_post(payload:dict = Body(...)):
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # here the new_post is a pydantic model
    # print(new_post)
    # pydantic model has a default method to convert the coming data into json format
    # print(new_post.model_dump())
    # post_dict = new_post.model_dump()
    # post_dict['id'] = randrange(0, 1000)
    # my_posts.append(post_dict)
    # return {
    #     'data': post_dict,
    #     'message': 'Post created successfully'
    # }
    # cursor.execute("""insert into posts (title,content,published) values(%s, %s, %s) returning *""",
    #                (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()
    # # to make the changes in the database
    # conn.commit()
    # post = models.Post(title=new_post.title, content=new_post.content,
    #                    published=new_post.published)
    # it will unpack the new_post
    post = models.Post(**new_post.model_dump())
    db.add(post)
    db.commit()
    # after commit the post will be a null value to restore the value to the variable post we use refresh
    db.refresh(post)
    return post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""delete from posts where id=%s returning *""", (str(id)),)
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter_by(id=id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} is not found')
    else:
        # synchronize_session=False means t's like saying, "No, don't update the list on the screen automatically. I'll refresh it myself later if I need to.
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    # x = find_post(id)
    # if x is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'post with id {id} is not found')
    # else:
    #     my_posts.remove(x)
    #     return Response(
    #         status_code=status.HTTP_204_NO_CONTENT
    #     )


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # x = find_post(id)
    # if x is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'Post with id {id} is not found')
    # else:
    #     index = my_posts.index(x)
    #     post_dict = post.model_dump()
    #     post_dict['id'] = id
    #     my_posts[index] = post_dict
    #     return {
    #         'data': post_dict,
    #         'msg': f'Post with id {id} updated successfully'
    #     }
    # cursor.execute("""update posts set title=%s,content=%s,published=%s where id=%s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter_by(id=id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} is not found')
    else:
        post_query.update(new_post.model_dump(), synchronize_session=False)
        db.commit()
        return post_query.first()
