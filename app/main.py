from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
# it is used to define schemas of the data that the user have to send to the server
from pydantic import BaseModel
from typing import Optional
from random import randrange
# module to use fastapi with postgres
import psycopg2
# it is used to access the column name while retreiving the data from the database
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# schema defenition while creating a post


class Post(BaseModel):
    title: str
    content: str
    # when the value is not given then True will be the default value
    published: bool = True
    # if not data is provided for the field rating then it will be none
    rating: Optional[int] = None


# we are using this while loop because once the connection failed try to connect again before executing the remaining codes.
while True:
    try:
        # cursor_factory=REalDictCursoe returns rows as dictionaries with column names as keys
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='abhidharsh@1999', cursor_factory=RealDictCursor)
        # The cursor object allows you to execute SQL queries
        cursor = conn.cursor()
        print('Database connected sucessfully')
        break
    except Exception as error:
        print('Database connection failed')
        print('Error: ', error)
        # it will wait for 2sec and try to connect again
        time.sleep(2)


my_posts = [{'id': 1, 'title': 'Statuatory warning', 'content': 'Smoking is injurious to health'},
            {'id': 2, 'title': 'I love to eat', 'content': 'Shawai is my favorite food'}]


@app.get("/")
def read_root():
    return {"Hello": "Worlds"}


@app.get('/posts')
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


def find_post(id):
    for i in range(len(my_posts)):
        x = my_posts[i]
        if x['id'] == id:
            return x
    return None


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    # x = find_post(id)
    # if x is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'Post with id:{id} not found')
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'msg':f'Post with id:{id} not found'}
    # else:
    #     response.status_code = status.HTTP_200_OK
    #     return {'data': x}
    cursor.execute("""select * from posts where id=%s""", (str(id)),)
    post = cursor.fetchone()
    return {'data': post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
# the parameter will convert the body into dict format and assign it to the variable payload
# def create_post(payload:dict = Body(...)):
def create_post(new_post: Post):
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
    cursor.execute("""insert into posts (title,content,published) values(%s, %s, %s) returning *""",
                   (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    # to make the changes in the database
    conn.commit()
    return {'data': post}


@app.delete('/posts/{id}')
def delete_post(id: int, response: Response):
    cursor.execute("""delete from posts where id=%s returning *""", (str(id)),)
    post = cursor.fetchone()
    conn.commit()
    return {'data': post}
    # x = find_post(id)
    # if x is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'post with id {id} is not found')
    # else:
    #     my_posts.remove(x)
    #     return Response(
    #         status_code=status.HTTP_204_NO_CONTENT
    #     )


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
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
    cursor.execute("""update posts set title=%s,content=%s,published=%s where id=%s returning *""",
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    return {'data': post}
