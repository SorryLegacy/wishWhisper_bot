"""Add wish model

Revision ID: af5984e87154
Revises: 752cacb5ae6a
Create Date: 2024-04-11 21:12:08.220515

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "af5984e87154"
down_revision: Union[str, None] = "752cacb5ae6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "wish_wish",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("prioritet", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("wish_wish")
    # ### end Alembic commands ###