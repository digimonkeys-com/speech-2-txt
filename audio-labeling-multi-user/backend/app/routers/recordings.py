from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from fastapi import File, Form

import os

from db.database import get_db
from models.recording import Recording
from utils.convert import convert_and_save_file
from schemas import user_schemas, info
from auth.jwt_helper import get_current_user

router = APIRouter(prefix=f"{os.getenv('ROOT_PATH')}/v1", tags=["Recordings"])


@router.post(
    "/recording",
    status_code=status.HTTP_200_OK,
    response_model=info.Info
)
async def store_recorded_sample(
        file: bytes = File(),
        browser: str = Form(),
        id: int = Form(),
        db: Session = Depends(get_db),
        current_user: user_schemas.User = Depends(get_current_user),
):

    if not os.path.exists("data/temp"):
        os.mkdir("data/temp")

    recording = Recording.get_recording_by_user_id_and_sample_id(db, id, current_user)

    filename, location, duration = convert_and_save_file(id,
                                                         browser, file,
                                                         current_user)

    if recording:
        current_user.total_duration += duration
        recording.is_recorded = True
        db.commit()
    else:
        return {"info": f"Sample with ID {id} for user {current_user.id} doesn't exist.'"}

    return {"info": f"file saved at '{location}'"}
