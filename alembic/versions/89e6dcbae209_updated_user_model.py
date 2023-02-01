"""updated user model

Revision ID: 89e6dcbae209
Revises: c8d041ddb277
Create Date: 2023-02-02 00:52:34.310648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89e6dcbae209'
down_revision = 'c8d041ddb277'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('middleName', sa.String(), nullable=True))
    op.add_column('users', sa.Column('coverPicUrl', sa.String(), nullable=True))
    op.add_column('users', sa.Column('appVersion', sa.String(), nullable=True))
    op.add_column('users', sa.Column('isLoggedIn', sa.Integer(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('currentLocation', sa.String(), nullable=True))
    op.add_column('users', sa.Column('latitude', sa.String(), nullable=True))
    op.add_column('users', sa.Column('longitude', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'longitude')
    op.drop_column('users', 'latitude')
    op.drop_column('users', 'currentLocation')
    op.drop_column('users', 'isLoggedIn')
    op.drop_column('users', 'appVersion')
    op.drop_column('users', 'coverPicUrl')
    op.drop_column('users', 'middleName')
    # ### end Alembic commands ###