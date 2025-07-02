"""Make _password_hash nullable in users table

Revision ID: nullable_password_hash
Revises: 
Create Date: 2024-06-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'nullable_password_hash'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('users', '_password_hash',
               existing_type=sa.String(),
               nullable=True)

def downgrade():
    op.alter_column('users', '_password_hash',
               existing_type=sa.String(),
               nullable=False)
