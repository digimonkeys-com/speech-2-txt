from fastapi import APIRouter, status, Depends, Response
from db.database import get_db
from sqlalchemy.orm import Session

from schemas.raw_text import RawText
from models.sample import Sample

router = APIRouter(tags=["Texts"], prefix='/api')


@router.post(
    "/texts",
    status_code=status.HTTP_200_OK
)
async def add_texts(
        text: RawText,
        db: Session = Depends(get_db)
):

    sentences = text.content.split(". ")
    samples = []
    for sentence in sentences:
        samples.append(Sample(transcription=(sentence + '.')))

    db.add_all(samples)
    db.commit()

    for n in samples:
        db.refresh(n)

    return {"message": samples}
