from os import listdir, mkdir

TMP_FOLDER = "tmp"

def create_tmp_folder() -> None:
    if TMP_FOLDER not in listdir():
        mkdir(TMP_FOLDER)
