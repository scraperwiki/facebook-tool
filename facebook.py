#!/usr/bin/env/python
# encoding: utf-8
import requests
import json
import sys
import urllib


def main(token):
    access_token = token
    base_url = 'https://graph.facebook.com/v2.0/fql'

    # get post details from Reese's page
    #query = "SELECT fromid, text, time, post_id FROM comment WHERE post_id in (SELECT post_id FROM stream WHERE source_id IN (SELECT page_id FROM page WHERE username='reeses'))"

    query = """{"comments": "SELECT fromid, text, time, post_id FROM comment WHERE post_id in (SELECT post_id FROM stream WHERE source_id IN (SELECT page_id FROM page WHERE username='reeses'))","names":"select uid,name from user where uid in (SELECT fromid FROM #comments)"}"""
    url = '{0}?q={1}&access_token={2}'.format(base_url, urllib.quote(query),
                                              access_token)
    print url
    content = requests.get(url).json()
    print json.dumps(content, indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
