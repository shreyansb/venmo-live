"""
This is a simple example of WebSocket + Tornado + Redis Pub/Sub usage.
Do not forget to replace YOURSERVER by the correct value.
Keep in mind that you need the *very latest* version of your web browser.
You also need to add Jacob Kristhammar's websocket implementation to Tornado:
Grab it here:
    http://gist.github.com/526746
Or clone my fork of Tornado with websocket included:
    http://github.com/kizlum/tornado
Oh and the Pub/Sub protocol is only available in Redis 2.0.0:
    http://code.google.com/p/redis/downloads/detail?name=redis-2.0.0-rc4.tar.gz

Tested with Chrome 6.0.490.1 dev under OS X.

For questions / feedback / coffee -> @kizlum or thomas@pelletier.im.
Have fun.
"""
import os

import tornado.autoreload
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


# This is ugly but I did not want to create multiple files for a so trivial
# example.

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/venmolive_new.html");

if __name__ == "__main__":
    settings = {
        #"static_path": "/Users/muffs/venmo-other/venmo-live",
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    application = tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)
    application.listen(8888)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
