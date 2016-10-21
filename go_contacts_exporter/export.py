import requests
import json
from sqlalchemy import create_engine
import click


def get_contacts(base_url, token, cursor=None, page_through=False):
    if cursor:
        url = '%s?cursor=%s' % (base_url, cursor)
    else:
        url = base_url
    while True:
        response = requests.get(url, headers={
            'Authorization': 'Bearer %s' % (token,)
        })
        page = response.json()
        cursor = page['cursor']
        for contact in page.get('data', []):
            yield (cursor, contact)
        if cursor and page_through:
            url = '%s?cursor=%s' % (base_url, cursor)
        else:
            break


@click.command()
@click.option('--token', help='The OAuth bearer token')
@click.option('--cursor', help='The cursor to continue from')
@click.option('--engine', help='The SQLAlchemy engine to use')
@click.option('--page/--no-page', default=True,
              help='Automatically page through with the cursor or not.')
@click.option('--base-url', help='The Contacts API URL',
              default='https://go.vumi.org/api/v1/go/contacts/')
def export_contacts(token, cursor, engine, page, base_url):
    from .tables import contacts
    if not engine:
        raise click.ClickException('engine parameter is required.')

    engine = create_engine(engine)
    if not engine.dialect.has_table(engine, 'contacts'):
        raise click.ClickException('contacts table is missing from database')
    connection = engine.connect()
    counter = 0
    for cursor, contact in get_contacts(base_url, token,
                                        cursor=cursor, page_through=page):
        try:
            trans = connection.begin()
            connection.execute(contacts.insert(),
                               key=contact['key'],
                               cursor=cursor,
                               msisdn=contact.get('msisdn'),
                               json=json.dumps(contact))
            trans.commit()
            click.secho('%s' % (counter,), fg='green')
            counter += 1
        except:
            trans.rollback()
            raise

if __name__ == '__main__':
    export_contacts()
