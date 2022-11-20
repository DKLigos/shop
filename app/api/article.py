from select import select
from typing import List, Optional

from fastapi import Depends, APIRouter, UploadFile, File, HTTPException
from pydantic import condecimal
from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession

from app.const import const
from app.deps.db_deps import get_db
from app.models import Article, ArticleLinkFileStorage, FileStorage
from app.schemas import ArticlesRemove

from app.crud.crud_article import article as crud_article
from app.crud.crud_file_storage import file_storage as crud_file_storage
from app.crud.crud_article_link_file_storage import article_link_file_storage as crud_article_link_file_storage
from app.utils import delete_file
from app.utils.upload_file import SignerFileUpload

router = APIRouter(prefix='/article', tags=['Товарные позиции [article]'])

sql_query_article = """Select * from shop.t_article ta
left join shop.t_article_link_file_storage talfs on ta.id_art = talfs.id_art
left join shop.t_file_storage tfs on tfs.id_file = talfs.id_file
where talfs.position = 0"""


@router.post("/get", summary='Возвращает товарные позиции')
async def get_article(db: AsyncSession = Depends(get_db)):  # noqa: B008
    result = await db.execute(select(Article.id_art
                                     , Article.name
                                     , Article.code
                                     , Article.price
                                     , Article.is_active
                                     , Article.description
                                     , FileStorage.full_path.label("img")
                                     , FileStorage.id_file)
                              .select_from(
        join(Article, ArticleLinkFileStorage, Article.id_art == ArticleLinkFileStorage.id_art))
                              .join(FileStorage, ArticleLinkFileStorage.id_file == FileStorage.id_file)
                              .filter(ArticleLinkFileStorage.position == 0))
    result = result.fetchall()

    return result


@router.post("/get_by_id/{id_art}", summary='Возвращает товарные позиции')
async def get_by_id(id_art: int, db: AsyncSession = Depends(get_db)):  # noqa: B008

    item = await crud_article.get(db=db, id_art=id_art)
    if not item:
        raise HTTPException(status_code=422,
                            detail="Данные не существуют.")
    result = await db.execute(select(Article.id_art
                                     , Article.name
                                     , Article.code
                                     , Article.price
                                     , Article.is_active
                                     , Article.description
                                     , ArticleLinkFileStorage.position
                                     , FileStorage.full_path
                                     , FileStorage.id_file)
                              .select_from(
        join(Article, ArticleLinkFileStorage, Article.id_art == ArticleLinkFileStorage.id_art))
                              .join(FileStorage, ArticleLinkFileStorage.id_file == FileStorage.id_file)
                              .filter(ArticleLinkFileStorage.id_art == id_art))
    result = result.fetchall()
    art_image = {}
    arts = []
    right_result = []
    for item in result:
        if item.position == 0:
            arts.append(item)
        if art_image.get(item.id_art):
            new_art = art_image.get(item.id_art)
            new_art[item.position] = item.full_path
            art_image.update({item.id_art: new_art})
        else:
            art_image.update({item.id_art: {item.position: item.full_path}})
    for art in arts:
        right_result.append({
            'id_art': art.id_art,
            'name': art.name,
            'code': art.code,
            'is_active': art.is_active,
            'price': art.price,
            'description': art.description,
            'imgs': art_image.get(art.id_art)
        })

    return right_result


@router.post("/create", summary='Добавить товар')
async def create_article(
        name: str,
        code: str,
        price: condecimal(max_digits=18, decimal_places=2),
        description: str,
        is_active: Optional[bool],
        files: List[UploadFile] = File(...),
        db: AsyncSession = Depends(get_db)):
    id_fiels = []
    for item in files:
        file_signature = SignerFileUpload(item, const.ALLOW_PICTURE_FORMATS)
        file_signature = await file_signature.save_in_database(db)
        id_fiels.append({'id_file': file_signature.id_file})

    check_unique = await crud_article.get(db, Article.code == code)

    if check_unique:
        raise HTTPException(status_code=422,
                            detail="Периоды действия доверенности пересекаются!")
    data = {
        'name': name,
        'code': code,
        'price': price,
        'description': description,
        'is_active': is_active,
    }
    article = await crud_article.create_from_data(db, obj_in_data=data)

    for item in id_fiels:
        art_link = ArticleLinkFileStorage(**{
            'id_art': article.id_art,
            'id_file': item.get('id_file'),
            'position': item.get('id_file')
        })
        db.add(art_link)
    await db.commit()

    return True


@router.post("/remove", summary='Удалить товары')
async def remove_article(ids: ArticlesRemove, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FileStorage.full_path, FileStorage.id_file)
                              .select_from(
        join(ArticleLinkFileStorage, FileStorage, ArticleLinkFileStorage.id_file == FileStorage.id_file))
                              .filter(ArticleLinkFileStorage.id_art.in_(ids.id_articles)))
    result = result.fetchall()
    id_files = [item.id_file for item in result]
    for item in result:
        delete_file.delete_file_from_uploads(item.full_path)

    await crud_article_link_file_storage.remove(db, ArticleLinkFileStorage.id_file.in_(id_files))
    await crud_file_storage.remove(db, FileStorage.id_file.in_(id_files))

    return await crud_article.remove(db, Article.id_art.in_(ids.id_articles))
