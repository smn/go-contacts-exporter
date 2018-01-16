from sqlalchemy import Table, MetaData, Column, String, JSON

metadata = MetaData()

contacts = Table(
    'contacts', metadata,
    Column('key', String(32), primary_key=True),
    Column('cursor', String(64)),
    Column('msisdn', String(255)),
    Column('json', JSON),
)

groups = Table(
    'groups', metadata,
    Column('key', String(32), primary_key=True),
    Column('cursor', String(64)),
    Column('name', String(255)),
    Column('json', JSON),
)
