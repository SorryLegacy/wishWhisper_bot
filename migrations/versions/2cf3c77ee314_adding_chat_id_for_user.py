"""Adding chat_id for user

Revision ID: 2cf3c77ee314
Revises: d339f1bb85c7
Create Date: 2024-04-02 21:49:22.061071

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2cf3c77ee314"
down_revision: Union[str, None] = "d339f1bb85c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user_user", sa.Column("chat_id", sa.BigInteger(), autoincrement=False, nullable=False))
    op.create_index(op.f("ix_user_user_chat_id"), "user_user", ["chat_id"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_user_chat_id"), table_name="user_user")
    op.drop_column("user_user", "chat_id")
    # ### end Alembic commands ###