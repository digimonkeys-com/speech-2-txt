"""create table samples

Revision ID: 3aafe6b5d39a
Revises: fea2f6b47829
Create Date: 2022-08-26 12:05:28.028046

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey

# revision identifiers, used by Alembic.
revision = '3aafe6b5d39a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('sample',
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("transcription", String(100000), nullable=False),
                    Column("filename", String(100000), nullable=True, unique=True)
                    )


def downgrade() -> None:
    pass
