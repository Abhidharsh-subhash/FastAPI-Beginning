from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get('/posts')
    def validate(post):
        return schemas.PostOut(**post)
    posts_map=map(validate,res.json())
    post_list=list(posts_map)
    assert len(test_posts) == len(res.json())
    assert res.status_code == 200
    # assert post_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get('/posts')
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/888888')
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    # assert post.Post['id'] == test_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title,content,published",[
    ('hello title','hello content',True),
    ('hii title','hii content',False),
    ('who title','who content',True)
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res = authorized_client.post('/posts',json={'title':title,'content':content,'published':published})
    new_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner_id == test_user['id']

def test_create_post_published_default_true(authorized_client,test_user):
    res = authorized_client.post('/posts',json={'title':'default title','content':'default content'})
    new_post = schemas.Post(**res.json())
    assert new_post.published == True

def test_unauthorized_user_create_post(client):
    res = client.post('/posts',json={'title':'default title','content':'default content'})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post_success(test_user,authorized_client,test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_non_exist(test_user,authorized_client,test_posts):
    res = authorized_client.delete('/posts/100000000')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403

def test_update_post(authorized_client,test_posts):
    data = {'title':'updated title','content':'updated content'}
    res = authorized_client.put(f'/posts/{test_posts[0].id}',json=data)
    post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert post.title == data['title']
    assert post.content == data['content']

def test_update_other_user_post(authorized_client,test_posts):
    data={'title':'updated title','content':'updated content'}
    res = authorized_client.put(f'/posts/{test_posts[3].id}',json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_posts):
    data={'title':'updated title','content':'updated content'}
    res = client.put(f'/posts/{test_posts[3].id}',json=data)
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client,test_posts):
    data={'title':'updated title','content':'updated content'}
    res = authorized_client.put('/posts/1000000000',json=data)
    assert res.status_code == 404
