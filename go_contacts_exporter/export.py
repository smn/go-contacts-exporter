import requests
import json

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
        for contact in page.get('data', []):
            yield contact
        if page['cursor'] and page_through:
            url = '%s?cursor=%s' % (base_url, page['cursor'])
            print 'paging to cursor: %s' % (page['cursor'],)
        else:
            break


@click.command()
@click.option('--token', help='The OAuth bearer token')
@click.option('--page/--no-page', default=True,
              help='Automatically page through with the cursor or not.')
@click.option('--base-url', help='The Contacts API URL',
              default='https://go.vumi.org/api/v1/go/contacts/')
def export_contacts(token, page, base_url):
    for contact in get_contacts(base_url, token, page_through=page):
        with open('contacts/%s.json' % (contact['key'],), 'w') as fp:
            json.dump(contact, fp)


if __name__ == '__main__':
    export_contacts()
