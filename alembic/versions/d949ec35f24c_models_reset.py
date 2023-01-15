"""models reset

Revision ID: d949ec35f24c
Revises: 
Create Date: 2023-01-13 23:49:51.583838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd949ec35f24c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('firstName', sa.String(), nullable=True),
    sa.Column('lastName', sa.String(), nullable=True),
    sa.Column('dateOfBirth', sa.String(), nullable=True),
    sa.Column('age', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('profilePicUrl', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('phoneVerified', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('emailVerified', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('isVerified', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('isBlocked', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('otpCode', sa.String(), nullable=True),
    sa.Column('deviceType', sa.String(), nullable=True),
    sa.Column('lastLogin', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('workEmail', sa.String(), nullable=True),
    sa.Column('profileType', sa.Integer(), nullable=True),
    sa.Column('requisitionId', sa.Integer(), nullable=True),
    sa.Column('profileId', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recruiter_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jobTitle', sa.String(), nullable=True),
    sa.Column('companyName', sa.String(), nullable=True),
    sa.Column('industry', sa.String(), nullable=True),
    sa.Column('noticePeriod', sa.String(), nullable=True),
    sa.Column('websiteUrl', sa.String(), nullable=True),
    sa.Column('linkedInUrl', sa.String(), nullable=True),
    sa.Column('otherUrl', sa.String(), nullable=True),
    sa.Column('profilePicUrl', sa.String(), nullable=True),
    sa.Column('bannerPicUrl', sa.String(), nullable=True),
    sa.Column('hiringRoleTitle', sa.String(), nullable=True),
    sa.Column('hiringRoleDescription', sa.String(), nullable=True),
    sa.Column('lastLogin', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('ratings', sa.Integer(), nullable=True),
    sa.Column('reviews', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('recruiter_profile')
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
