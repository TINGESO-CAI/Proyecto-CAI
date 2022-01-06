"""agregarcuenta

Revision ID: 04fc079610ae
Revises: 2bc5c3656406
Create Date: 2022-01-06 15:34:06.015442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04fc079610ae'
down_revision = '2bc5c3656406'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cuenta',
    sa.Column('id_cuenta', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('correo', sa.Text(), nullable=True),
    sa.Column('contrasena', sa.Text(), nullable=True),
    sa.Column('nombre', sa.Text(), nullable=True),
    sa.Column('apellido', sa.Text(), nullable=True),
    sa.Column('rut', sa.Text(), nullable=True),
    sa.Column('rol', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id_cuenta')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cuenta')
    # ### end Alembic commands ###
