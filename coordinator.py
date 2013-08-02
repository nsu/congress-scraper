from TwitterListGenerator import TwitterListGenerator
from TwitterStreamWatcher import TwitterStreamWatcher
import gevent

politician_lists = ['cspan/senators', 'cspan/u-s-representatives', 'cspan/governors', 'subterraneus/standardnews']

politician_ids = []
for twitter_list in politician_lists:    
    politician_ids += TwitterListGenerator(twitter_list).get_ids()

watcher = TwitterStreamWatcher(politician_ids)
watcher.watch_stream()
