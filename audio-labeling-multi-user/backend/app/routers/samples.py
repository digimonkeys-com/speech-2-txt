from fastapi import APIRouter, status, Depends
from db.database import get_db
from sqlalchemy.orm import Session
import os

from models.user_model import User
from models.sample import Sample
from models.recording import Recording
from schemas import user_schemas, info
from auth.jwt_helper import get_current_user
from schemas.raw_text import RawText

router = APIRouter(prefix=f"{os.getenv('ROOT_PATH')}/v1", tags=["Samples"])


@router.post(
    "/sample",
    status_code=status.HTTP_200_OK
)
async def add_samples(
        text: RawText,
        db: Session = Depends(get_db),
        current_user: user_schemas.User = Depends(get_current_user)
):
    sentences = text.content.split(". ")
    samples = []
    for sentence in sentences:
        samples.append(Sample(transcription=(sentence + '.')))

    db.add_all(samples)
    db.commit()
    db.begin()

    for n in samples:
        db.refresh(n)

    users = User.get_all_users(db)
    to_create = []
    for sample in samples:
        for user in users:
            to_create.append(Recording(sample_id=sample.id, user_id=user.id))

    db.add_all(to_create)
    db.commit()

    return {"message": f"{len(samples)} samples created."}


@router.get(
    "/sample",
    status_code=status.HTTP_200_OK,

)
async def get_unrecorded_sample(
        db: Session = Depends(get_db),
        current_user: user_schemas.User = Depends(get_current_user)
):
    record = db.query(Recording).filter(
        Recording.user_id == current_user.id,
        Recording.is_recorded.is_(None)
    ).first()

    sample = db.query(Sample).filter(Sample.id == record.sample_id).first()

    return {'sample': sample}


@router.delete(
    "/sample/{id}",
    status_code=status.HTTP_200_OK,
    response_model=info.Info)
async def delete_sample(
        db: Session = Depends(get_db),
        current_user: user_schemas.User = Depends(get_current_user),
        id: int = 1
):
    db.query(Sample).filter(Sample.id == id).delete()
    db.commit()

    return {'info': f'Sample with id {id} deleted'}


def create_recordings_for_user(db, user):
    samples = Sample.get_all_samples(db)
    to_create = []
    for sample in samples:
        record = db.query(Recording).filter(
            Recording.sample_id == sample.id,
            Recording.user_id == user.id
        ).first()

        if not record:
            to_create.append(Recording(user_id=user.id, sample_id=sample.id))

    db.add_all(to_create)
    db.commit()

    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(f"data/{user.id}"):
        os.mkdir(f"data/{user.id}")
