"""t_m2

Revision ID: 386af5fb453b
Revises: 14057e32129f
Create Date: 2023-05-17 22:19:03.206484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '386af5fb453b'
down_revision = '14057e32129f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tag_to_image_image_id_fkey', 'tag_to_image', type_='foreignkey')
    op.drop_constraint('tag_to_image_tag_id_fkey', 'tag_to_image', type_='foreignkey')
    op.create_foreign_key(None, 'tag_to_image', 'images', ['image_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'tag_to_image', 'tags', ['tag_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag_to_image', type_='foreignkey')
    op.drop_constraint(None, 'tag_to_image', type_='foreignkey')
    op.create_foreign_key('tag_to_image_tag_id_fkey', 'tag_to_image', 'tags', ['tag_id'], ['id'])
    op.create_foreign_key('tag_to_image_image_id_fkey', 'tag_to_image', 'images', ['image_id'], ['id'])
    # ### end Alembic commands ###
