from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
# it is used to define schemas of the data that the user have to send to the server
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# schema defenition while creating a post


class Post(BaseModel):
    title: str
    content: str
    # when the value is not given then True will be the default value
    published: bool = True
    # if not data is provided for the field rating then it will be none
    rating: Optional[int] = None


my_posts = [{'id': 1, 'title': 'Statuatory warning', 'content': 'Smoking is injurious to health'},
            {'id': 2, 'title': 'I love to eat', 'content': 'Shawai is my favorite food'}]


@app.get("/")
def read_root():
    return {"Hello": "Worlds"}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


def find_post(id):
    for i in range(len(my_posts)):
        x = my_posts[i]
        if x['id'] == id:
            return x
    return None


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    x = find_post(id)
    if x is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg':f'Post with id:{id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'data': x}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
# the parameter will convert the body into dict format and assign it to the variable payload
# def create_post(payload:dict = Body(...)):
def create_post(new_post: Post):
    # here the new_post is a pydantic model
    # print(new_post)
    # pydantic model has a default method to convert the coming data into json format
    # print(new_post.model_dump())
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0, 1000)
    my_posts.append(post_dict)
    return {
        'data': post_dict,
        'message': 'Post created successfully'
    }


@app.delete('/posts/{id}')
def delete_post(id: int, response: Response):
    x = find_post(id)
    if x is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} is not found')
    else:
        my_posts.remove(x)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    x = find_post(id)
    if x is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} is not found')
    else:
        index = my_posts.index(x)
        post_dict = post.model_dump()
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {
            'data': post_dict,
            'msg': f'Post with id {id} updated successfully'
        }
