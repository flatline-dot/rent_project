"""move on new_flat

Revision ID: 466d4b37c743
Revises: 328c495f6160
Create Date: 2021-08-03 15:43:05.641599

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '466d4b37c743'
down_revision = '328c495f6160'
branch_labels = None
depends_on = None


def upgrade():
    query = """
    INSERT INTO new__flat (num_rooms,
                          floor,
                          link,
                          area,
                          material,
                          metro,
                          district,
                          street,
                          price,
                          commission,
                          deposit)
    SELECT flat.num_rooms,
           flat.floor,
           flat.link,
           flat.area,
           flat.material,
           location.metro,
           location.district,
           location.street,
           payment.price,
           payment.commission,
           payment.deposit
    FROM flat
         INNER JOIN location ON flat.location_id = location.id
         INNER JOIN payment ON flat.payment_id = payment.id"""

    op.execute(query)


def downgrade():
    pass
