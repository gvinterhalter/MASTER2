"""init

Revision ID: f227700e0f82
Revises: 
Create Date: 2017-11-05 22:05:50.099748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f227700e0f82'
down_revision = None
branch_labels = None
depends_on = None

from sqlalchemy import SmallInteger


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('go_ontology',
    sa.Column('ontology', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('ontology', name=op.f('pk_go_ontology'))
    )
    op.create_table('predictor',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name', name=op.f('pk_predictor'))
    )
    op.create_table('sequence',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('sequence', sa.Text(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('predictable', sa.Boolean(), nullable=True),
    sa.CheckConstraint('char_length(sequence) = length', name=op.f('ck_sequence_length')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sequence'))
    )
    op.create_table('disorder_prediction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sequence_id', sa.String(), nullable=True),
    sa.Column('predictor_name', sa.String(), nullable=True),
    sa.Column('is_disordered', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['predictor_name'], ['predictor.name'], name=op.f('fk_disorder_prediction_predictor_name_predictor')),
    sa.ForeignKeyConstraint(['sequence_id'], ['sequence.id'], name=op.f('fk_disorder_prediction_sequence_id_sequence')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_disorder_prediction')),
    sa.UniqueConstraint('predictor_name', name=op.f('uq_disorder_prediction_predictor_name')),
    sa.UniqueConstraint('sequence_id', name=op.f('uq_disorder_prediction_sequence_id'))
    )
    op.create_table('go_term',
    sa.Column('go', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('ontology', sa.String(length=1), nullable=False),
    sa.ForeignKeyConstraint(['ontology'], ['go_ontology.ontology'], name=op.f('fk_go_term_ontology_go_ontology')),
    sa.PrimaryKeyConstraint('go', name=op.f('pk_go_term'))
    )
    op.create_table('disorder_prediction_raw',
    sa.Column('pr_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.ARRAY(SmallInteger()), nullable=True),
    sa.ForeignKeyConstraint(['pr_id'], ['disorder_prediction.id'], name=op.f('fk_disorder_prediction_raw_pr_id_disorder_prediction'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('pr_id', name=op.f('pk_disorder_prediction_raw'))
    )
    op.create_table('disorder_prediction_regions',
    sa.Column('dp_id', sa.Integer(), nullable=False),
    sa.Column('region', sa.SmallInteger(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['dp_id'], ['disorder_prediction.id'], name=op.f('fk_disorder_prediction_regions_dp_id_disorder_prediction'), ondelete='cascade'),
    sa.PrimaryKeyConstraint('dp_id', 'region', name=op.f('pk_disorder_prediction_regions'))
    )
    op.create_table('sequence_go_assoc',
    sa.Column('sequence_id', sa.String(), nullable=False),
    sa.Column('go', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['go'], ['go_term.go'], name=op.f('fk_sequence_go_assoc_go_go_term')),
    sa.ForeignKeyConstraint(['sequence_id'], ['sequence.id'], name=op.f('fk_sequence_go_assoc_sequence_id_sequence')),
    sa.PrimaryKeyConstraint('sequence_id', 'go', name=op.f('pk_sequence_go_assoc'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sequence_go_assoc')
    op.drop_table('disorder_prediction_regions')
    op.drop_table('disorder_prediction_raw')
    op.drop_table('go_term')
    op.drop_table('disorder_prediction')
    op.drop_table('sequence')
    op.drop_table('predictor')
    op.drop_table('go_ontology')
    # ### end Alembic commands ###