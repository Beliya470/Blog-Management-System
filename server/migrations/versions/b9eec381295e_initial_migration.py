from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'b9eec381295e'
down_revision = None
branch_labels = None
depends_on = None

def does_table_exist(table_name):
    """
    Utility function to check if a table already exists in the current database.
    """
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    return inspector.has_table(table_name)


def upgrade():
    # Only create the 'blog_post' table if it doesn't already exist.
    if not does_table_exist('blog_post'):
        op.create_table(
            'blog_post',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('content', sa.String(length=1000), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Only create the 'review' table if it doesn't already exist.
    if not does_table_exist('review'):
        op.create_table(
            'review',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('content', sa.String(length=500), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('blogpost_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['blogpost_id'], ['blog_post.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade():
    # Here, we handle the 'downgrade' operation.
    # We drop the 'review' and 'blog_post' tables if they exist, without touching the 'user' table.
    if does_table_exist('review'):
        op.drop_table('review')
    
    if does_table_exist('blog_post'):
        op.drop_table('blog_post')
