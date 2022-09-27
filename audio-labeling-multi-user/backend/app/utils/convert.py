from fastapi import HTTPException
import soundfile as sf
import librosa

import subprocess
import os


def convert_and_save_file(id_: str, browser: str, file: bytes, user):

    dir_ = f"data/{user.id}/{id_}"

    try:
        os.mkdir(dir_)
    except Exception as e:
        print(e)

    n = len(os.listdir(dir_)) + 1

    final_filename = f"{n}.wav"
    final_file_location = f"{dir_}/{final_filename}"

    if browser == "chrome":
        temp_file_location = f"data/temp/{id_}_{user.id}.webm"

        with open(temp_file_location, "wb+") as file_object:
            file_object.write(file)

        command = ['ffmpeg', "-y", '-i', temp_file_location, final_file_location]
        subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    elif browser == "firefox":
        temp_file_location = f"data/temp/{id_}_{user.id}.ogg"

        with open(temp_file_location, "wb+") as file_object:
            file_object.write(file)

        data, samplerate = sf.read(temp_file_location)
        sf.write(final_file_location, data, samplerate)
    else:
        raise HTTPException(status_code=400, detail="Unsupported user agent")

    duration = librosa.get_duration(filename=temp_file_location)
    os.remove(temp_file_location)
    return final_filename, final_file_location, duration
