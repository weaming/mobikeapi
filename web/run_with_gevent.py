#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

from gevent import wsgi
from app import app


server = wsgi.WSGIServer(('', 5000), app)
server.serve_forever()
