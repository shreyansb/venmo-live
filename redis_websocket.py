"""
Shreyans Bhansali and Julian Connor
Venmo Hackathon, October 2011

Thanks to Thomas Pelletier (https://github.com/pelletier)
The base gist for this code is at: https://gist.github.com/532067
For questions / feedback / coffee -> @kizlum or thomas@pelletier.im.
Have fun.
"""

import os
import logging
import redis
import threading
import tornado.autoreload
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import venmo_live_settings

LISTENERS = []

def redis_listener():
    r = redis.Redis()
    sub = r.pubsub()
    channel_name = venmo_live_settings.CHANNEL_NAME
    sub.subscribe([channel_name])
    for message in sub.listen():
        for element in LISTENERS:
            element.write_message(unicode(message['data']))

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        pass
        #self.settings['static_url_prefix'] = '/live/static/'

class MainHandler(BaseHandler):
    def get(self):
        self.render("templates/venmolive.html")

class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        # check to see if the websocket is authenticated
        logging.info(self)
        logging.info(self.get_cookie('sessionid'))
        LISTENERS.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        LISTENERS.remove(self)

settings = {
    'auto_reload': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/realtime/', RealtimeHandler),
], **settings)


if __name__ == "__main__":
    threading.Thread(target=redis_listener).start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9700)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
