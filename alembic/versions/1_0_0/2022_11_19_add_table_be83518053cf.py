"""add table

Revision ID: be83518053cf
Revises: 
Create Date: 2022-11-19 18:43:17.199850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be83518053cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_article',
    sa.Column('id_art', sa.Integer(), nullable=False, comment='ID товара'),
    sa.Column('name', sa.String(length=60), nullable=False, comment='Наименование товара'),
    sa.Column('code', sa.String(length=60), nullable=False, comment='Код товара'),
    sa.Column('price', sa.Integer(), nullable=False, comment='Цена товара'),
    sa.Column('description', sa.String(), nullable=True, comment='Описание товара'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='Присутствие товара'),
    sa.PrimaryKeyConstraint('id_art', name=op.f('pk_t_article')),
    schema='shop'
    )
    op.create_index(op.f('ix_shop_t_article_id_art'), 't_article', ['id_art'], unique=False, schema='shop')
    op.create_table('t_file_storage',
    sa.Column('id_file', sa.Integer(), nullable=False, comment='ID'),
    sa.Column('name_file', sa.String(length=100), nullable=False, comment='Имя файла'),
    sa.Column('full_path', sa.String(length=255), nullable=False, comment='Путь к файлу'),
    sa.PrimaryKeyConstraint('id_file', name=op.f('pk_t_file_storage')),
    schema='shop',
    comment='Хранилище файлов'
    )
    op.create_index(op.f('ix_shop_t_file_storage_id_file'), 't_file_storage', ['id_file'], unique=False, schema='shop')
    op.create_table('t_user',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id_user', name=op.f('pk_t_user')),
    schema='shop'
    )
    op.create_index(op.f('ix_shop_t_user_id_user'), 't_user', ['id_user'], unique=False, schema='shop')
    op.create_table('t_article_link_file_storage',
    sa.Column('id', sa.Integer(), nullable=False, comment='ID'),
    sa.Column('id_art', sa.Integer(), nullable=False, comment='ID товара'),
    sa.Column('id_file', sa.Integer(), nullable=False, comment='ID файла'),
    sa.Column('position', sa.Integer(), nullable=False, comment='Позиция фотографии'),
    sa.ForeignKeyConstraint(['id_art'], ['shop.t_article.id_art'], name=op.f('fk_t_article_link_file_storage_id_art_t_article')),
    sa.ForeignKeyConstraint(['id_file'], ['shop.t_file_storage.id_file'], name=op.f('fk_t_article_link_file_storage_id_file_t_file_storage')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_t_article_link_file_storage')),
    schema='shop',
    comment='Таблица связи товара и фото'
    )
    op.create_index(op.f('ix_shop_t_article_link_file_storage_id'), 't_article_link_file_storage', ['id'], unique=False, schema='shop')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shop_t_article_link_file_storage_id'), table_name='t_article_link_file_storage', schema='shop')
    op.drop_table('t_article_link_file_storage', schema='shop')
    op.drop_index(op.f('ix_shop_t_user_id_user'), table_name='t_user', schema='shop')
    op.drop_table('t_user', schema='shop')
    op.drop_index(op.f('ix_shop_t_file_storage_id_file'), table_name='t_file_storage', schema='shop')
    op.drop_table('t_file_storage', schema='shop')
    op.drop_index(op.f('ix_shop_t_article_id_art'), table_name='t_article', schema='shop')
    op.drop_table('t_article', schema='shop')
    # ### end Alembic commands ###
