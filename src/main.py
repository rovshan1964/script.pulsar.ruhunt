# -*- coding: utf-8 -*-

import re, urllib

from pulsar import provider

RE = {
    'block': re.compile("<td class='small inner'>(.+?)</tr>", re.S),
    'uri': re.compile('<a href="(magnet[^"]+)"', re.S),
    'name': re.compile("""<a href='http[^>]+title="([^"]+)">""", re.S),
    'seeders': re.compile("<span class='seeders'[^>]+>([0-9]+)<"),
    'leechers': re.compile("<span class='leechers'[^>]+>([0-9]+)<")
}


def search(query):
    response = provider.GET('http://ruhunt.org/search', params={
        'q': query.encode('utf8'),
        'i': 's',
        'tag': 'video',
        'load': '1',
        'sort': 'peers_desc',
        #'tracker': '2'
    })
    result = []
    for line in RE['block'].findall(response.data):
        uri = RE['uri'].search(line)
        if uri:
            name = RE['name'].search(line)
            if name:
                r = RE['seeders'].search(line)
                seeders = int(r.group(1)) if r else 0
                r = RE['leechers'].search(line)
                leechers = int(r.group(1)) if r else 0
                result.append({
                    'uri': uri.group(1),
                    'name': name.group(1),
                    'seeds': seeders,
                    'peers': seeders + leechers,
                    #'size': 1024*1024*1024,
                    'language': 'ru'

                    # TODO: все что ниже оставленно до лучших времен
                    # 'resolution': 'int',
                    # 'video_codec': 'int',
                    # 'audio_codec': 'int',
                    # 'rip_type': 'int',
                    # 'scene_rating': 'int',
                    #'trackers': [], TODO: надо разобраться что сюда пихать - толи просто домен серверов, то ли полный URL для анонса
                })
    print str(result)
    return result


def search_movie(movie):
    return search(u'{0} {1}'.format(movie['title'], movie['year']))


def search_episode(episode):
    print str(episode)
    return search(u'{0} сезон {1} серия {2}'.format(episode['title'], episode['season'], episode['episode']))


provider.register(search, search_movie, search_episode)
