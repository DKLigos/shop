import os

from app.core.config import settings


def delete_file_from_uploads(path):
    try:
        os.remove(settings.PROJECT_ROOT + path)
    except Exception as e:
        print(e)