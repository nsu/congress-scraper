import oauth2 as oauth
import time
import requests
import json

class TwitterListGenerator(object):
    def __init__(self, list_string):
        self.url = "https://api.twitter.com/1.1/lists/members.json"
        list_string = list_string.split('/')
        owner_screen_name = list_string[0]
        slug = list_string[1]

        self.params = {
            "cursor": -1,
            "owner_screen_name": owner_screen_name,
            "slug": slug,
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
        }
        
        self.user_ids = []
        
    def generate_request(self):
        token = oauth.Token(key="15968447-kXvllXQTckmhjjo1BsDg4a1i1yzrgAOa91X0jnnos", secret="cNKHn6BlS7THuvYhqwG5hnExUr60vOWXpZbMe3ml0U")
        consumer = oauth.Consumer(key="CGF0xXAheUZaASeqmOceSA", secret="mDW67qgJUzmOMosN2t9WPtifLCnQs5yePhkyiWEcs")
        self.params['oauth_token'] = token.key
        self.params['oauth_consumer_key'] = consumer.key
        #generate
        req = oauth.Request(method="GET", url=self.url, parameters=self.params)
        #sign
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, token)
        return req
    
    def get_ids(self):
        while self.params['cursor']:
            req = self.generate_request()
            resp = requests.get(req.to_url())
            print resp.headers
            resp = json.loads(resp.text)
            self.user_ids += [user['id'] for user in resp['users']]
            self.params['cursor'] = resp[ 'next_cursor' ]
        return [str(i) for i in self.user_ids]

if __name__ == '__main__':
    from time import sleep
    lists = ['cspan/senators', 'cspan/u-s-representatives', 'cspan/governors']
    ids = []
    for tw_list in lists:
        ids += TwitterListGenerator(tw_list).get_ids()
    base_url = "https://api.twitter.com/1/users/show.json?user_id="
    followers = []
    ids = [ids[0:99], ids[100:199], ids[200:299], ids[300:399], ids[400:499], ids[500:]]
    for idlist in ids:
        for id in idlist:
            reqData = requests.get("".join([base_url, id]))
            reqData = json.loads(reqData.text)
            screen_name = reqData['screen_name']
            follow_count = reqData["followers_count"]
            next_user = {'screen_name': screen_name, 'followers': follow_count} 
            followers.append(next_user)
        sleep(60*60)
    print json.dumps(followers)
