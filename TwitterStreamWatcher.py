import oauth2 as oauth
import time
import requests
import json
import couchdb

class TwitterStreamWatcher(object):
    def __init__(self, id_list):
        self.url = "https://stream.twitter.com/1.1/statuses/filter.json"
        self.db = couchdb.Server()['psc208']
        self.id_list = id_list
        follow_ids = ",".join(id_list)

        self.params = {
            "follow": follow_ids,
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
        req = oauth.Request(method="POST", url=self.url, parameters=self.params)
        #sign
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, token)
        return req
    
    def watch_stream(self):
        req = self.generate_request()
        resp = requests.post(req.to_url(), stream=True)
        for line in resp.iter_lines():
            if line: # filter out keep-alive new lines
                print line
                hydrated = json.loads(line)
                if 'user' in hydrated and hydrated['user']['id_str'] in self.id_list:
                    print hydrated['user']['screen_name']
                    self.db.save(hydrated)
                
                
    
