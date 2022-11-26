# -*- coding: utf-8 -*-
import os
import inspect
from uuid import uuid4
import asyncio
from aiofile import async_open
import logging
from app.const import const
from app.exceptions.upload_file import (CreateDirException, NoFilePartException, NoSelectedFile,
                                        NotAllowedFormatException)
from app.models import FileStorage
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import file_storage as crud_file_storage
from fastapi import HTTPException

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.DEBUG)


class Uploader:
    def __init__(self, name, directory):
        self.file_name = name
        self.path_directory = directory
        self.__full_path_name = None

    @property
    def full_path_without_root_prefix(self):
        return self.full_path_name.replace(settings.PROJECT_ROOT, '')

    @property
    def full_path_name(self):
        if self.__full_path_name is None:
            full_path_with_name = os.path.join(self.path_directory, self.file_name)
            if os.path.exists(full_path_with_name):
                path_and_extensions = full_path_with_name.split('.')
                path_and_extensions.insert(1, str(uuid4())[:7])
                self.__full_path_name = '.'.join(path_and_extensions)
            else:
                self.__full_path_name = full_path_with_name
        return self.__full_path_name


class FileUpload(Uploader):
    def __init__(self, file, directory, allow_extensions=None):
        super().__init__(file.filename, directory)
        self.file = file
        self.allow_extensions = allow_extensions or const.ALLOW_ALL_FORMATS

    def get_verbose_name_with_format(self, verbose_name):
        if verbose_name is None:
            return
        extension = os.path.splitext(self.full_path_name)[1]
        verbose_name = os.path.splitext(verbose_name)[0]
        return f"{verbose_name}{extension}"

    async def save_in_database(self, db: AsyncSession, verbose_name_file=None) -> FileStorage:
        await self.upload_in_storage()
        name =  self.get_verbose_name_with_format(verbose_name_file) or self.file_name
        file = await crud_file_storage.create(db, obj_in={
            'name_file': self.get_verbose_name_with_format(verbose_name_file) or self.file_name,
            'full_path': self.full_path_without_root_prefix,
            'url': settings.URL + '/img/' + name
        })
        return file

    async def __upload_in_storage(self):
        if not self.file.file:
            raise NoFilePartException
        if self.file.filename == '':
            raise NoSelectedFile
        if not self.is_allowed_file_extension():
            raise NotAllowedFormatException

        create_directory_if_not_exist(self.path_directory)

        async with async_open(self.full_path_name, 'wb') as fout:

            if inspect.iscoroutinefunction(self.file.file.read):
                while True:
                    await asyncio.sleep(0)
                    chunk = await self.file.file.read(100000)
                    if not chunk:
                        break
                    await fout.write(chunk)
            else:
                while True:
                    await asyncio.sleep(0)
                    chunk = self.file.file.read(100000)
                    if not chunk:
                        break
                    await fout.write(chunk)
        return self

    async def upload_in_storage(self):
        try:
            return await self.__upload_in_storage()
        except CreateDirException:
            raise HTTPException(status_code=400, detail="Произошла ошибка при создании папки")
        except NotAllowedFormatException:
            raise HTTPException(status_code=400, detail=f"Файл {self.file_name} имеет неподходящий формат ")
        except (NoFilePartException, NoSelectedFile):
            raise HTTPException(status_code=400, detail="Не выбран файл")

    def is_allowed_file_extension(self):
        return self.file.filename.split('.')[-1] in self.allow_extensions


class SignerFileUpload(FileUpload):
    def __init__(self, file, allow_extensions=None):
        super().__init__(file, directory=settings.SIGNER_DIR_PATH, allow_extensions=allow_extensions)


def create_directory_if_not_exist(path_directory):
    if not os.path.exists(path_directory):
        try:
            os.makedirs(path_directory, exist_ok=True)
        except Exception:
            logging.error(f"Ошибка создания папки - {path_directory}", exc_info=True)
            raise CreateDirException
