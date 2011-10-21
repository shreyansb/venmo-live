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
import threading
import tornado.autoreload
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import redis
import venmo_live_settings


# This is ugly but I did not want to create multiple files for a so trivial
# example.
TEMPLATE = """
<!DOCTYPE>
<html>
<head>
    <title>Sample test</title>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.4.2.min.js"></script>
</head>
<body>
    <div id="log"></div>
    <script type="text/javascript" charset="utf-8">
        $(document).ready(function(){
            if ("WebSocket" in window) {
              var ws = new WebSocket("ws://ec2-50-16-101-124.compute-1.amazonaws.com/realtime/");
              ws.onopen = function() {};
              ws.onmessage = function (evt) {
                  var received_msg = evt.data;
                  var html = $("#log").html();
                  html += "<p>"+received_msg+"</p>";
                  $("#log").html(html);
              };
              ws.onclose = function() {};
            } else {
              alert("WebSocket not supported");
            }
        });
    </script>
</body>
</html>
"""


LISTENERS = []


def redis_listener():
    r = redis.Redis()
    sub = r.pubsub()
    channel_name = venmo_live_settings.CHANNEL_NAME
    sub.subscribe([channel_name])
    for message in sub.listen():
        for element in LISTENERS:
            element.write_message(unicode(message['data']))

class NewMsgHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test_template.html")

class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        LISTENERS.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        LISTENERS.remove(self)

settings = {
    'auto_reload': True,
}

application = tornado.web.Application([
    (r'/', NewMsgHandler),
    (r'/realtime/', RealtimeHandler),
], **settings)


if __name__ == "__main__":
    threading.Thread(target=redis_listener).start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
