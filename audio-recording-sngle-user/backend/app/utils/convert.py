import moviepy.editor as moviepy
from fastapi import HTTPException
import soundfile as sf
import subprocess


def convert_and_save_file(id: str, browser: str, file: bytes):
    final_filename = f"{id}.wav"
    final_file_location = f"data/{final_filename}"

    if browser == "chrome":
        temp_file_location = f"data/temp/{id}.webm"

        with open(temp_file_location, "wb+") as file_object:
            file_object.write(file)

        command = ['ffmpeg', "-y", '-i', temp_file_location, final_file_location]
        subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    elif browser == "firefox":
        temp_file_location = f"data/temp/{id}.ogg"

        with open(temp_file_location, "wb+") as file_object:
            file_object.write(file)

        data, samplerate = sf.read(temp_file_location)
        sf.write(final_file_location, data, samplerate)
    else:
        raise HTTPException(status_code=400, detail="Unsupported user agent")

    return final_filename, final_file_location
