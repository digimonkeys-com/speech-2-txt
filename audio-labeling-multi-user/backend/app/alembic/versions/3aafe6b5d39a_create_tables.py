"""create table samples

Revision ID: 3aafe6b5d39a
Revises: fea2f6b47829
Create Date: 2022-08-26 12:05:28.028046

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String,\
    PrimaryKeyConstraint, UniqueConstraint, Boolean
import sqlalchemy_utils
from auth.hash import Hash


# revision identifiers, used by Alembic.
revision = '3aafe6b5d39a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('sample',
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("transcription", String(100000), nullable=False)
                    )

    users_table = op.create_table(
        'user',
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
        Column('password', sa.Text()),
        Column('name', sa.String(length=32), nullable=False),
        Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        Column('total_duration', Integer),
        PrimaryKeyConstraint('id'),
        UniqueConstraint('email')
    )

    op.bulk_insert(
        users_table,
        [
            {
                "email": "test@test.com",
                "password": Hash.get_password_hash("test"),
                "name": "Test",
                'total_duration': 0
            }
        ]
    )

    op.create_table(
        'recording',
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("sample_id", Integer, nullable=False),
        Column("user_id", Integer, nullable=False),
        Column('is_recorded', Boolean)
    )


def downgrade() -> None:
    pass
