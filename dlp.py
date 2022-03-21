#!/usr/bin/python3

import argparse
import feedparser
import questionary
import requests

import StripTags
#
# parser = argparse.ArgumentParser(prog='dlp', description='Podcast Downloader')
# parser.add_argument('-f','--feed', help='URL of podcast\' RSS feed')
# parser.add_argument('-p','--podcasts', nargs='?', help='Select from list of podcasts [in file -p FILENAME]')
# parser.add_argument('-e','--episodes', help='Select episodes from podcast', action='store_true')
# parser.add_argument('-l','--list', nargs='?', help='List available podcast episodes', type=int, default=True)
# parser.add_argument('-d','--download', nargs='?', help='Download latest N podcast episodes', type=int)
# args = parser.parse_args()
#
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
        print('[title]:      ', entry['title'])
        print('[published]:  ', entry['published'])
        print('[summary]:    ', StripTags.strip_tags(entry['summary']))
        print('[content[0]]: ', StripTags.strip_tags(entry['content'][0]['value']))
        print('[content[1]]: ', StripTags.strip_tags(entry['content'][1]['value']))
        print('[href]:       ', entry['enclosures'][0].href)

def download_episodes(episodes):
    episodes = get_episodes(rss_url)
    for entry in episodes[0:args.download]:
        print('downloading: ', entry['title'], ' --> ', entry['enclosures'][0].href)
        filename = str(entry['enclosures'][0].href).split('/')[-1]; print(filename)
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

# if args.episodes:
#     episodes = get_episodes(rss_url)
#     selected_episodes = select_episodes(episodes)
#
#     for e in selected_episodes:
#         i = int(e.split()[0])
#         print('[title]:     ', episodes[i]['title'])
#         print('[published]: ', episodes[i]['published'])
#         print('[summary]:   ', episodes[i]['summary'])
#         print('[content]:   ', episodes[i]['content'])
#         print('[duration]:  ', episodes[i]['itunes_duration'])
#         print('[href]:      ', episodes[i]['enclosures'][0].href)

if args.quiet == False:
    episodes = get_episodes(rss_url)
    selected_episodes = select_episodes(episodes)
    list_episodes(selected_episodes)
    # for entry in episodes[0:args.quiet]:
        # for item in entry.items():
        #     print(item)
        # print(entry['title'])
        # print('[published]: ', entry['published'])
        # print('[summary]: ', entry['summary'])
        # print('[content]: ', entry['content'])
        # print('[duration]: ', entry['itunes_duration'])
        # print('[href]: ', entry['enclosures'][0].href)

if args.download:
    episodes = get_episodes(rss_url)
    for entry in episodes:
        print('downloading: ', entry['title'], '\nURL: ', entry['enclosures'][0].href)
        filename = str(entry['enclosures'][0].href).split('/')[-1]; print(filename)
        dlreq = requests.get(entry['enclosures'][0].href)
        with open(filename, 'wb') as dl:
            dl.write(dlreq.content)
