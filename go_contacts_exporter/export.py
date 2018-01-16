import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import click

session = requests.Session()
session.headers.update({
    'Connection': 'keep-alive',
})


def get_records(url, token, cursor=None, page_through=False):
    while True:
        if cursor:
            api_url = '%s?cursor=%s' % (url, cursor)
        else:
            api_url = url

        response = session.get(api_url, headers={
            'Authorization': 'Bearer %s' % (token,)
        })
        page = response.json()
        new_cursor = page.get('cursor', -1)
        for contact in page.get('data', []):
            yield (cursor, contact)
        if new_cursor != -1 and page_through:
            click.secho("Fetching next cursor %s" % (new_cursor,))
            cursor = new_cursor
        elif new_cursor is None:
            click.secho("Looks like we're done!")
        else:
            click.secho("Crashed but retrying %s" % (cursor,), fg='red')
            url = url
            # break


def get_contacts(base_url, token, cursor=None, page_through=False):
    return get_records("%scontacts/" % (base_url,),
                       token, cursor, page_through)


def get_groups(base_url, token, cursor=None, page_through=False):
    return get_records("%sgroups/" % (base_url,),
                       token, cursor, page_through)


@click.group()
def export():
    pass


@export.command()
@click.option('--token', help='The OAuth bearer token')
@click.option('--cursor', help='The cursor to continue from')
@click.option('--engine', help='The SQLAlchemy engine to use')
@click.option('--page/--no-page', default=True,
              help='Automatically page through with the cursor or not.')
@click.option('--base-url', help='The Contacts API URL',
              default='http://localhost:8300/api/v1/go/')
def contacts(token, cursor, engine, page, base_url):
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
            click.secho(
                '%s - %s - %s' % (counter, cursor, contact['key']), fg='green')
            counter += 1
        except(IntegrityError,):
            click.secho("Contact %s already exists." % (contact['key']), fg='blue')
            trans.rollback()
            continue
        except:
            trans.rollback()
            raise


@export.command()
@click.option('--token', help='The OAuth bearer token')
@click.option('--cursor', help='The cursor to continue from')
@click.option('--engine', help='The SQLAlchemy engine to use')
@click.option('--page/--no-page', default=True,
              help='Automatically page through with the cursor or not.')
@click.option('--base-url', help='The Contacts API URL',
              default='https://go.vumi.org/api/v1/go/')
def groups(token, cursor, engine, page, base_url):
    from .tables import groups
    if not engine:
        raise click.ClickException('engine parameter is required.')

    engine = create_engine(engine)
    if not engine.dialect.has_table(engine, 'groups'):
        raise click.ClickException('groups table is missing from database')
    connection = engine.connect()
    counter = 0
    for cursor, group in get_groups(base_url, token,
                                    cursor=cursor, page_through=page):
        try:
            trans = connection.begin()
            connection.execute(groups.insert(),
                               key=group['key'],
                               cursor=cursor,
                               name=group.get('name'),
                               json=json.dumps(group))
            trans.commit()
            click.secho(
                '%s - %s - %s' % (counter, cursor, group['key']), fg='green')
            counter += 1
        except:
            trans.rollback()
            raise


if __name__ == '__main__':
    export()
