"""create users table

Revision ID: a7e20cba9f50
Revises:
Create Date: 2024-04-13 12:32:34.839895

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a7e20cba9f50"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "botusers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ChatID", sa.BigInteger(), nullable=False),
        sa.Column("Name", sa.String(length=255), nullable=True),
        sa.Column("Lastname", sa.String(length=255), nullable=True),
        sa.Column("Username", sa.String(length=255), nullable=True),
        sa.Column("ReferralCode", sa.BigInteger(), nullable=True),
        sa.Column("ReferredBy", sa.BigInteger(), nullable=True),
        sa.Column("ReferralCount", sa.Integer(), nullable=False),
        sa.Column("ReferralLink", sa.String(length=255), nullable=True),
        sa.Column("PrefLanguage", sa.String(length=255), nullable=True),
        sa.Column(
            "CreatedAt",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "UpdatedAt",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_botusers_ChatID"), "botusers", ["ChatID"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_botusers_ChatID"), table_name="botusers")
    op.drop_table("botusers")
    # ### end Alembic commands ###
