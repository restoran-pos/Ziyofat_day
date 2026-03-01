"""change table status enum

Revision ID: dda04903e2ff
Revises: 1055116bf7a5
Create Date: 2026-03-01 07:00:44.860868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dda04903e2ff'
down_revision: Union[str, Sequence[str], None] = '1055116bf7a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_status = sa.Enum("free", "occupied", "reserved", name="table_status")

def upgrade():
    bind = op.get_bind()

    # 1) enum type yaratish
    table_status.create(bind, checkfirst=True)

    # 2) column type'ni enumga o‘tkazish
    op.alter_column(
        "dining_table",
        "status",
        existing_type=sa.String(),
        type_=table_status,
        postgresql_using="status::table_status",
        nullable=False,
        server_default="free",
    )


def downgrade():
    bind = op.get_bind()

    # 1) qaytadan stringga o‘tkazish
    op.alter_column(
        "dining_table",
        "status",
        existing_type=table_status,
        type_=sa.String(),
        nullable=True,
        server_default=None,
    )

    # 2) enum type'ni o‘chirish
    table_status.drop(bind, checkfirst=True)