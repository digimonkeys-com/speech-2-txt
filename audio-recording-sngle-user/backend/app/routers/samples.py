from fastapi import APIRouter, status, Depends, Response
from fastapi import FastAPI, File, Form, Header
from fastapi.responses import StreamingResponse, FileResponse
from db.database import get_db
from sqlalchemy.orm import Session
import librosa
import pandas as pd

import os
import tarfile
import shutil

from schemas.status import Status
from models.sample import Sample
from utils.convert import convert_and_save_file

if not os.path.exists("data"):
    os.mkdir("data")

router = APIRouter(tags=["Samples"], prefix="/api")


@router.get(
    "/unrecorded_samples/{n}",
    status_code=status.HTTP_200_OK
)
async def get_unrecorded_samples(
        db: Session = Depends(get_db),
        n: int = 1
):
    res = Sample.get_unrecorded_samples(db, n)

    return {'samples': res}


@router.post(
    "/unrecorded_samples",
    status_code=status.HTTP_200_OK
)
async def store_recorded_sample(
        file: bytes = File(),
        browser: str = Form(),
        id: int = Form(),
        db: Session = Depends(get_db)
):

    if not os.path.exists("data/temp"):
        os.mkdir("data/temp")

    filename, location = convert_and_save_file(id, browser, file)

    sample = Sample.get_sample_by_id(db, id)
    if sample:
        sample.filename = filename
        db.commit()
    else:
        return {"info": f"Sample with ID {id} doesn't exist.'"}

    return {"info": f"file saved at '{location}'"}

@router.delete(
    "/unrecorded_samples/{id}",
    status_code=status.HTTP_200_OK
)
async def get_unrecorded_samples(
        db: Session = Depends(get_db),
        id: int = 1
):
    db.query(Sample).filter(Sample.id == id).delete()
    db.commit()

    return {'info': f'Sample with id {id} deleted'}


@router.get(
    "/status",
    status_code=status.HTTP_200_OK
)
async def get_status(
        db: Session = Depends(get_db)
):
    duration = 0
    for item in os.listdir("data"):
        if item not in  ["temp", ".gitkeep"]:
            duration += librosa.get_duration(filename=f"data/{item}")

    recorded_samples = db.query(Sample).filter(Sample.filename.is_not(None)).count()
    total_samples = db.query(Sample).count()
    return {'duration': duration / 60, 'samples': total_samples,
            "unrecorded_samples": total_samples - recorded_samples,
            "recorded_samples": recorded_samples}


@router.get(
    "/download",
    status_code=status.HTTP_200_OK,
    response_model=Status
)
async def download_data(
        db: Session = Depends(get_db)
):
    data = db.query(Sample).all()

    try:
        shutil.rmtree("data/temp/")
    except:
        # rmtree will raise exception when temp folder do not exist
        # I added try block to tell it to STFU
        pass

    path_to_csv = "labels.csv"
    path_to_tar = "data.tar.gz"
    df = pd.DataFrame([item.to_dict() for item in data])
    df.to_csv(path_to_csv)

    with tarfile.open(path_to_tar, "w:gz") as tar:
        tar.add(path_to_csv, arcname='labels.csv')
        tar.add("data", arcname="data")

    def iterfile():
        with open(path_to_tar, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="application/x-tar")
    # return {'file': FileResponse(path_to_tar, filename="data.tar.gz")}
