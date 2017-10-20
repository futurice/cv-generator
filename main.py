#!/usr/bin/env python3

import cherrypy
import weasyprint
from jinja2 import Template, FileSystemLoader, Environment
from base64 import b64encode
import os
import json
import random
import psycopg2
import base64

class App(object):

    def __init__(self):
        loader = FileSystemLoader('templates')
        self.templateEnv = Environment(loader =  loader)
        connString = os.environ.get("POSTGRES_CONNECTION", "dbname=cvgenerator user=cvgenerator")
        self.baseUrl = os.environ.get("BASE_URL", "")
        self.conn = psycopg2.connect(connString)
        self.conn.autocommit = True
        cur = self.getCursor()
        cur.execute('CREATE TABLE IF NOT EXISTS cvdata (key TEXT PRIMARY KEY, data JSON, picmimetype varchar(15), pic bytea);')


    def getCursor(self):
        return self.conn.cursor()

    def getData(self, key, cur):
        cur.execute('SELECT data FROM cvdata WHERE key = %s', (key, ))
        s = cur.fetchone()

        if s == None or s[0] == None:
            data = {}
        else:
            data = s[0]

        return data

    def ensureKey(self, key, cur):
        try:
            cur.execute('INSERT INTO cvdata (key) values (%s)', (key, ))
        except psycopg2.IntegrityError:
            pass

    def setData(self, key, data, cur):
        self.ensureKey(key, cur)
        cur.execute('UPDATE cvdata SET data = %s WHERE key = %s', (data, key))


    def getPic(self, key, cur):
        cur.execute('SELECT picmimetype, pic FROM cvdata where key = %s', (key, ))
        mimetype, picBytes = cur.fetchone()
        if mimetype == None:
            return None
        else:
            foo =  'data:%s;base64,%s' % (mimetype, base64.b64encode(picBytes).decode('utf-8'))
            print(foo[0:100])
            return foo


    def setPic(self, key, picMimeType, picBytes, cur):
        self.ensureKey(key, cur)
        cur.execute('UPDATE cvdata SET picmimetype = %s, pic = %s WHERE key = %s', (picMimeType, picBytes, key))

    @cherrypy.expose('cv')
    @cherrypy.tools.json_in()
    def cv(self, **kwargs):
        cur = self.getCursor()
        isPng = kwargs['type'] == 'png'
        doBase64 = kwargs.get('base64') != None
        if (isPng):
            responseType = 'application/png'
        else:
            responseType = 'application/pdf'


        key = kwargs['key']
        try: # get from request and persist if request contains, otherwise get from db
            data = cherrypy.request.json
            self.setData(key, json.dumps(data), cur)
        except AttributeError:
            data = self.getData(key, cur)

        savedPicDataUri = self.getPic(key, cur)

        if savedPicDataUri != None:
            data['image'] = savedPicDataUri
        else:
            data['image'] = 'placeholder.jpg'

        cherrypy.response.headers['Content-Type'] = responseType
        template = self.templateEnv.get_template('cv.html')
        style = weasyprint.CSS(string = """
        .pic {
          height: 979px;
          z-index: -1;
          width: 800px;
          margin: 0;
        }

        .logo {
          width: 120px;
          position: fixed;
          left: 850px;
          bottom: 50px;
        }

        .intro-texts {
          min-height: 220px;
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
          font-family: Futurice Bold;
          width: 800px;
          bottom: 50px;
          left: 50px;
        }

        .social span {
          display: block;
        }

        .right-pane {
          box-sizing: border-box;
          position: absolute;
          left: 1064px;
          top: 50px;
          margin: 0;
          height: 1080px;
        }

        .left-pane {
          position: relative;
          left: 50px;
          top: 50px;
          margin: 0;
          padding: 0;
          width: 984px;
          height: 1080px;
        }

        dt {
          font-family: Futurice Bold;
          margin-top: 30px;
        }

        dd {
          margin-left: 0;
        }

        h1.name {
          font-family: Futurice Regular;
          padding-top: 0px;
          padding-bottom: 10px;
          margin-top: 0;
          margin-bottom: 0;
        }

        .title {
          margin-top: 15px;
          font-family: Futurice Regular;
        }

        .color-background {
          background-color: #F9FAFB;
          z-index: -6;
          width: 5000px;
          height: 5000px;
          transform: rotate(30deg);
          position: fixed;
          left: 200px;
          top: 0;
        }

        h1, h2, h3 {
          letter-spacing: 2px;
        }

        h3 {
          font-family: Futurice Bold;
        }


        body {
          background-color: white;
          font-family: Futurice Regular;
          color: #452999;
          font-size: 30px;
          line-height: 1.2em;
          width: 1920px;
          height: 1080px;
          overflow: hidden;
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

        if isPng:
            extension = 'png'
        else:
            extension = 'pdf'

        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename=cv.' + extension + ';'

        if doBase64:
            return b64encode(bytes)
        else:
            return bytes

    @cherrypy.expose('')
    def index(self, **kwargs):
        cur = self.getCursor()
        try:
            key = kwargs['key']
        except KeyError:
            raise cherrypy.HTTPRedirect('%s/?key=%08x' % (self.baseUrl, random.getrandbits(32)))

        data = self.getData(key, cur)

        return self.templateEnv.get_template('index.html').render(data)


    @cherrypy.expose('upload')
    def upload(self, **kwargs):
        cur = self.getCursor()
        key = kwargs['key']
        self.setPic(key, kwargs['mimetype'], cherrypy.request.body.read(), cur)


cherrypy.quickstart(App(), '/',
                    {'/style.css':
                     {'tools.staticfile.on': True,
                      'tools.staticfile.filename': os.getcwd() + '/style.css'
                     },
                     '/index.js':
                     {'tools.staticfile.on': True,
                      'tools.staticfile.filename': os.getcwd() + '/index.js'
                     },
                     '/futurice-favicon.png':
                     {'tools.staticfile.on': True,
                      'tools.staticfile.filename': os.getcwd() + '/futurice-favicon.png'
                     },
                     'global': {
                         'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8000
                     }
                    })
