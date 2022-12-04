"""Initialize metadata table

Revision ID: 01779ca112b4
Revises: 
Create Date: 2022-12-04 13:28:51.322886

"""
from alembic import op
import sqlalchemy as sa


revision = '01779ca112b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'metadata',
        sa.Column('id', sa.String(100), primary_key=True),
        sa.Column('imports', sa.Integer, nullable=False),
        sa.Column('exports', sa.Integer, nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('size', sa.String(100), nullable=False),
        sa.Column('type', sa.String(15), nullable=False),
        sa.Column('arch', sa.String(3), nullable=False),
    )

def downgrade():
    op.drop_table('metadata')
