"""Add chat secret to user

Revision ID: 601f74ad117e
Revises: 151d99799d68
Create Date: 2021-08-26 01:59:10.462162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "601f74ad117e"
down_revision = "151d99799d68"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("chat_embed_secret", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "chat_embed_secret")
    # ### end Alembic commands ###