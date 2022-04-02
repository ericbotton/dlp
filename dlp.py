#!/usr/bin/python3

import argparse
import feedparser
import questionary
import requests

from striptags import strip_tags

parser = argparse.ArgumentParser(prog='dlp', description='Podcast Downloader')
parser.add_argument('-f','--feed', nargs='?', help='URL of podcast\' RSS feed')
parser.add_argument('-p','--podcasts', nargs='?', help='Select from list of podcasts in file [-p FILENAME]', default=True)
# parser.add_argument('-e','--episodes', nargs='?', help='Select episodes from podcast', default=False)
parser.add_argument('-q','--quiet', nargs='?', help='Do not list podcast episode details', default=False)
parser.add_argument('-d','--download', nargs='?', help='Download selected podcast episodes', default=False)
args = parser.parse_args()

# default podcast filename: dlp.list
podcast_list_filename = 'dlp.list'

def get_podcast_list(filename):
    podcast_list = []
    with open(filename) as f:
        for l in f:
            podcast_list.append(l.strip())

    return podcast_list

def get_episodes(rss_url):
    episodes = []
    parsed_rss = feedparser.parse(rss_url)
    for entry in parsed_rss.entries:
        episodes.append(entry)
    return episodes

def select_from_file(filename):
    podcast_list = get_podcast_list(filename)

    selected_podcast = questionary.select("Select your podcast...", choices=podcast_list).ask()

    return selected_podcast

def select_episodes(episodes):
    episode_details = []
    for i in range(len(episodes)):
        episode_details.append(str(i) + ' - ' + episodes[i]['title'] + '|' + episodes[i]['published'])        # print(details)

    selected_strings = questionary.checkbox("Select your episodes...", choices=episode_details).ask()

    selected_episodes = []
    for e in selected_strings:
        i = int(e.split()[0])
        selected_episodes.append(episodes[i])

    return selected_episodes

def list_episodes(episodes):
    for entry in episodes:
        print('[title]:       ', entry['title'])
        print('[published]:   ', entry['published'])
        print('[summary]:     ', strip_tags(entry['summary']))
        print('[description]: ', strip_tags(entry['description']))
#       print('[content[0]]:  ', strip_tags(entry['content'][0]['value']))
#       print('[content[1]]:  ', strip_tags(entry['content'][1]['value']))
        print('[href]:        ', entry['enclosures'][0].href)

def rename_filename(filename):
    forbiden_characters = '<>:"/|\?*&'
    for replace_character in forbiden_characters:
        filename = filename.replace(replace_character, '_')
    return filename

def download_episode(entry):
    filename = str(entry['enclosures'][0].href).split('/')[-1]
    filename = rename_filename(filename)
    print(filename)
    dlreq = requests.get(entry['enclosures'][0].href)
    with open(filename, 'wb') as dl:
        dl.write(dlreq.content)

print('| feed=' + str(args.feed),
 '| podcasts=' + str(args.podcasts),
  '| quiet=' + str(args.quiet),
   '| download=' + str(args.download))

if not args.feed:
    if args.podcasts == True or args.podcasts == None:
        podcast_list_filename = 'dlp.list'
    else:
        podcast_list_filename = args.podcasts

    selected_podcast = select_from_file(podcast_list_filename)
    rss_url = selected_podcast.split()[0]

else:
    rss_url = args.feed
print(rss_url)

episodes = get_episodes(rss_url)
selected_episodes = select_episodes(episodes)

if args.quiet == False:
    list_episodes(selected_episodes)

if args.download != False:
    for entry in selected_episodes:
        print('downloading: ', entry['title'], '\nURL: ', entry['enclosures'][0].href)
        download_episode(entry)

