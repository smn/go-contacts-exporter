from sqlalchemy import create_engine
import click


@click.command()
@click.option('--engine', help='The SQLAlchemy engine to use.')
def init_db(engine):
    if not engine:
        raise click.ClickException('engine parameter is required.')
    from .tables import contacts, groups
    engine = create_engine(engine)

    tables = [contacts, groups]

    for table in tables:
        if not engine.dialect.has_table(engine, table.name):
            table.create(engine)
            click.secho('%s table created.' % (table.name,), fg='green')
        else:
            click.secho('%s table already exists.' % (table.name,), fg='red')


if __name__ == '__main__':
    init_db()
