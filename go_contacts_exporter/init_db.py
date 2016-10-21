from sqlalchemy import create_engine
import click


@click.command()
@click.option('--engine', help='The SQLAlchemy engine to use.')
def init_db(engine):
    if not engine:
        raise click.ClickException('engine parameter is required.')
    from .tables import contacts
    engine = create_engine(engine)
    if not engine.dialect.has_table(engine, 'contacts'):
        contacts.create(engine)
        click.secho('Contacts table created.', fg='green')
    else:
        click.secho('Contacts table already exists.', fg='red')


if __name__ == '__main__':
    init_db()
