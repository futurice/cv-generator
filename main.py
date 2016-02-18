#!/usr/bin/env python3

import cherrypy
import weasyprint
from jinja2 import Template, FileSystemLoader, Environment
from base64 import b64encode
import os
import redis
import json
import random

class App(object):

    def __init__(self):
        loader = FileSystemLoader('templates')
        self.templateEnv = Environment(loader =  loader)
        self.redis = redis.Redis(host="localhost")

    @cherrypy.expose('cv')
    @cherrypy.tools.json_in()
    def cv(self, **kwargs):
        data = cherrypy.request.json
        isPng = kwargs['type'] == 'png'
        doBase64 = kwargs.get('base64') != None
        if (isPng):
            responseType = 'application/png'
        else:
            responseType = 'application/pdf'


        key = kwargs['key']
        self.redis.set(key, json.dumps(data))
        savedFilenameMaybe = self.redis.get(key + '-filename')

        if savedFilenameMaybe != None:
            data['image'] = savedFilenameMaybe.decode('utf-8')
        else:
            data['image'] = 'placeholder.jpg'

        cherrypy.response.headers['Content-Type'] = responseType
        template = self.templateEnv.get_template('cv.html')
        style = weasyprint.CSS(string = """
        .pic {
          position: absolute;
          left: -8px;
          top: -8px;
          height: 1080px;
          z-index: -1;
          width: 726px;
          margin: 0;
        }

        .right-pane {
          position: absolute;
          left: 726px;
          top: 0;
          background-color: white;
          margin: 0;
          height: 1080px;
          padding-left: 50px;
          padding-top: 50px;
          padding-right: 200px;
        }

        .experience {
          float: left;
          width: 442px;
        }

        .education {
          float: left;
          width: 472px;
          padding-left: 30px;
        }

        .social {
          position: fixed;
          width: 472px;
          bottom: 50px;
          left: 1248px;
          color: green;
        }

        .social span {
          display: block;
        }

        .left-pane {
          position: relative;
          left: 0;
          top: 0;
          margin: 0;
          padding: 0;
          width: 726px;
          height: 1080px;
        }

        dt {
          font-family: Sharp Sans No1 Bold;
        }

        dd {
          margin-left: 0;
        }

        .keywords {
          position: absolute;
          left: 50%;
          margin-right: -50%;
          transform: translate(-50%, 0);
          bottom: 50px;
          background-color: #C4E2D9;
          padding-left: 10px;
          padding-right: 30px;
        }

        h1.name {
          padding-top: 0px;
          padding-bottom: 10px;
          margin-top: 0;
          margin-bottom: 0;
        }

        .title {
          margin-top: 0;
        }

        h1, h2, h3 {
          font-family: Sharp Sans No1 Black;
          letter-spacing: 1px;
        }

        h3 {
          text-transform: uppercase;
        }

        body {
          font-family: Sharp Sans No1 Medium;
          font-size: 30px;
        }

        @page {
          size: 1920px 1080px;
          margin: 0;
        }
        """)
        doc = weasyprint.HTML(base_url=".", string = template.render(data))
        if isPng:
            bytes = doc.write_png(target=None, stylesheets=[style])
        else:
            bytes =  doc.write_pdf(target=None, stylesheets=[style])

        if doBase64:
            return b64encode(bytes)
        else:
            return bytes

    @cherrypy.expose('')
    def index(self, **kwargs):
        try:
            key = kwargs['key']
        except KeyError:
            raise cherrypy.HTTPRedirect('/?key=%08x' % random.getrandbits(32))

        s = self.redis.get(key)

        if s == None:
            data = {'social': {}}
        else:
            data = json.loads(s.decode('utf-8'))

        return self.templateEnv.get_template('index.html').render(data)

    @cherrypy.expose('upload')
    def upload(self, **kwargs):
        filename = 'uploads/' + kwargs['filename']
        key = kwargs['key']
        self.redis.set(key + '-filename', filename)
        f = open(filename, 'wb')
        f.write(cherrypy.request.body.read())
        f.close


cherrypy.quickstart(App(), '/',
                    {'/style.css':
                     {'tools.staticfile.on': True,
                      'tools.staticfile.filename': os.getcwd() + '/style.css'
                     },
                     '/index.js':
                     {'tools.staticfile.on': True,
                      'tools.staticfile.filename': os.getcwd() + '/index.js'
                     },
                     'global': {
                         'server.socket_host': '0.0.0.0'
                     }
                    })
