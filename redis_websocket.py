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
import re
import redis
import threading
import tornado.auth
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
    
    def authenticate_user(self):
        session_email = self.get_secure_cookie('session_email')
        if not session_email:
            self.redirect('/auth/')
            return False
        if not self.is_session_email_authorized(session_email):
            self.clear_cookie('session_email')
            self.write('Sorry, you do not have access to this page')
            return False

    def is_session_email_authorized(self, email):
        allowed_email_regex = getattr(venmo_live_settings, 
                                      'ALLOWED_EMAIL_REGEX',
                                      None)
        if allowed_email_regex:
            if re.match(allowed_email_regex, email):
                return True
        if hasattr(venmo_live_settings, 'ALLOWED_EMAILS'):
            if email in venmo_live_settings.ALLOWED_EMAILS:
                return True
        return False

class MainHandler(BaseHandler):
    def get(self):
        if self.authenticate_user():
            self.render("templates/venmolive.html")
        else:
            return self.finish()

class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self.authenticate_user():
            LISTENERS.append(self)
        else:
            return self.finish()

    def on_message(self, message):
        pass

    def on_close(self):
        try:
            LISTENERS.remove(self)
        except ValueError:
            pass

class AuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        # Save the authenticated user's details in a secure cookie
        self.set_secure_cookie('session_email', user.get('email'))
        self.redirect('/')

settings = {
    'auto_reload': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret': venmo_live_settings.COOKIE_SECRET
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/realtime/', RealtimeHandler),
    (r'/auth/', AuthHandler),
], **settings)


if __name__ == "__main__":
    threading.Thread(target=redis_listener).start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
