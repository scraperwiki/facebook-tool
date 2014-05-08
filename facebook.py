#!/usr/bin/env/python
# encoding: utf-8
import requests
import json
import logging
import sys
import urllib


def parse_query_output(query_result_json):
    print type(query_result_json)

    for comment in query_result_json['data'][0]['fql_result_set']:
        print comment['fromid'], comment['post_id'], comment['time'], \
            comment['text']

    for user in query_result_json['data'][1]['fql_result_set']:
        print user['uid'], user['name']


def main(token):
    logging.basicConfig(level=logging.INFO)
    access_token = token
    base_url = 'https://graph.facebook.com/v2.0/fql'

    # get post details from Reese's page
    #query = "SELECT fromid, text, time, post_id FROM comment WHERE post_id in (SELECT post_id FROM stream WHERE source_id IN (SELECT page_id FROM page WHERE username='reeses'))"

    query = ("""{"comments": "SELECT fromid, text, time, post_fbid, post_id """
             """FROM comment WHERE post_id in """
             """(SELECT post_id FROM stream """
             """WHERE source_id IN (SELECT page_id FROM page """
             """WHERE username='reeses'))","""
             """"names":"select uid,name from user """
             """WHERE uid in (SELECT fromid FROM #comments)"}""")
    url = '{0}?q={1}&access_token={2}'.format(base_url, urllib.quote(query),
                                              access_token)
    content = requests.get(url).json()

    try:
        parse_query_output(content)
    except KeyError as e:
        logging.critical("No data found in JSON: {}".format(content))
        raise e

if __name__ == '__main__':
    main(sys.argv[1])
