#!/usr/bin/env/python
# encoding: utf-8
import json
import logging
import sys
import urllib

import requests
import scraperwiki


def parse_query_output(query_result_json):
    results = zip(query_result_json['data'][0]['fql_result_set'],
                  query_result_json['data'][1]['fql_result_set'])

    rows = []
    for result in results:
        data = {}
        data['from_id'] = result[0]['fromid']
        data['post_fbid'] = result[0]['post_fbid']
        data['post_id'] = result[0]['post_id']
        data['time'] = result[0]['time']
        data['text'] = result[0]['text']
        data['uid'] = result[1]['uid']
        data['name'] = result[1]['name']
        rows.append(data)

    logging.info("Got {0} rows.".format(len(rows)))
    scraperwiki.sqlite.save(unique_keys=['post_fbid'], data=rows)


def main(token, username):
    """ Look up first comment page(?) for account; save to database.

    python facebook.py <access_token> <username>
    """
    logging.basicConfig(level=logging.INFO)
    access_token = token
    base_url = 'https://graph.facebook.com/v2.0/fql'

    # get post details from Reese's page
    #query = "SELECT fromid, text, time, post_id FROM comment WHERE post_id in (SELECT post_id FROM stream WHERE source_id IN (SELECT page_id FROM page WHERE username='reeses'))"

    query = ("""{{"comments": """
             """"SELECT fromid, text, time, post_fbid, post_id """
             """FROM comment WHERE post_id in """
             """(SELECT post_id FROM stream """
             """WHERE source_id IN (SELECT page_id FROM page """
             """WHERE username='{}'))","""
             """"names":"select uid,name from user """
             """WHERE uid in (SELECT fromid """
             """FROM #comments)"}}""".format(username))
    url = '{0}?q={1}&access_token={2}'.format(base_url, urllib.quote(query),
                                              access_token)
    content = requests.get(url).json()

    try:
        parse_query_output(content)
    except KeyError as e:
        logging.critical("No data found in JSON: {}".format(content))
        raise e

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
