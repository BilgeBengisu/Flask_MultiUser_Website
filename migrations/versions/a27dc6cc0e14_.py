"""empty message

Revision ID: a27dc6cc0e14
Revises: 
Create Date: 2025-02-04 20:57:15.489688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a27dc6cc0e14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_image', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('wallpaper_image', sa.String(length=150), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('wallpaper_image')
        batch_op.drop_column('profile_image')

    # ### end Alembic commands ###
