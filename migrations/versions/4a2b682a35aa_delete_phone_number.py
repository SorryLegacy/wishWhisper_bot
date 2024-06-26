"""Delete phone number

Revision ID: 4a2b682a35aa
Revises: 2cf3c77ee314
Create Date: 2024-04-03 21:54:43.201505

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a2b682a35aa"
down_revision: Union[str, None] = "2cf3c77ee314"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_user_user_phone_number", table_name="user_user")
    op.drop_column("user_user", "phone_number")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user_user", sa.Column("phone_number", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_index("ix_user_user_phone_number", "user_user", ["phone_number"], unique=True)
    # ### end Alembic commands ###
