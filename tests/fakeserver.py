import flask
import multiprocessing
import logging
import time

class FakeServer:
    def __init__(self, debug=False):
        """
        Constructor
        @param debug show server debug (default = False). WARNING : could create some bug because of Flask debug mode
        """
        self.debug = debug
        self.callbacks = {}

        #Disable Flask logs
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def page_handler(self):
        url = flask.request.path
        if url in self.callbacks:
            args = {}
            for key in flask.request.args:
                args[key] = flask.request.args.get(key)

            response = {"content" : "Not Found", "status" : 404}
            for callback, params in self.callbacks[url]:
                res = True
                if params:
                    for key, val in params.iteritems():
                        if key not in args or args[key] != val:
                            res = False
                if res:
                    response = callback(args)

            if "status" not in response:
                response["status"] = 200
            return flask.make_response(response["content"], response["status"])
        return flask.make_response("404 Not Found", 404)

    def server_thread(self):
        """
        Threaded method for Flask server execution
        """
        app = flask.Flask(__name__)
        app.debug = self.debug

        app.error_handler_spec[None][404] = (lambda err: self.page_handler())

        app.run()

    def add_url_callback(self, url, callback, params=None):
        if not url in self.callbacks:
            self.callbacks[url] = []
        self.callbacks[url].append((callback, params))

    def start(self):
        """
        Start the server (async)
        """
        self.server = multiprocessing.Process(target=self.server_thread)
        self.server.start()
        time.sleep(0.5) # Let the server start, just in case...

    def stop(self):
        """
        Stop the server
        """
        self.server.terminate()
        self.server.join()


