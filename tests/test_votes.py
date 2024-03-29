import pytest
from app import models

#a fixture to vote for a post for the working purpose of test_vote_twice_post
#we are using session here as we are going to directly put the data into the table
@pytest.fixture
def test_vote(test_posts,session,test_user):
    new_vote = models.Vote(post_id=test_posts[3].id,user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client,test_posts):
    data = {'post_id':test_posts[0].id,'dir':1}
    res = authorized_client.post('/vote',json=data)
    assert res.status_code == 201

def test_vote_twice_post(authorized_client,test_posts,test_vote):
    data = {'post_id':test_posts[3].id,'dir':1}
    res = authorized_client.post('/vote',json=data)
    assert res.status_code == 409

def test_delete_vote(authorized_client,test_posts,test_vote):
    data = {'post_id':test_posts[3].id,'dir':0}
    res = authorized_client.post('/vote',json=data)
    assert res.status_code == 201

def test_delete_vote_non_exist(authorized_client,test_posts):
    data = {'post_id':test_posts[3].id,'dir':0}
    res = authorized_client.post('/vote',json=data)
    assert res.status_code == 404

# def test_vote_post_non_exist(authorized_client,test_posts):
#     data = {'post_id':100000000000,'dir':1}
#     res = authorized_client.post('/vote',json=data)
#     assert res.status_code == 404

def test_vote_unauthorized_user(client,test_posts):
    data = {'post_id':test_posts[3].id,'dir':1}
    res = client.post('/vote',json=data)
    res.status_code == 401
