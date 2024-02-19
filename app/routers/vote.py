from fastapi import APIRouter, status, Depends, HTTPException
from ..import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    vote_exist = db.query(models.Post).filter_by(id=vote.post_id).count()
    if not vote_exist:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'vote with the id {vote.post_id} does not exist')
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        else:
            new_vote = models.Vote(post_id=vote.post_id,
                                   user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {'msg': f'successfully voted for the post {vote.post_id}'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='vote does not exist')
        else:
            # db.delete(found_vote) if we need to delete the found_vote
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {'msg': 'Successfully deleted the vote'}
