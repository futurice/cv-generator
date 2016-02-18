#!/usr/bin/env python3

import cherrypy
import weasyprint
from jinja2 import Template, FileSystemLoader, Environment

class App(object):
    @cherrypy.expose('cv')
    @cherrypy.tools.json_in()
    def cv(self, **kwargs):
        loader = FileSystemLoader('templates')
        templateEnv = Environment(loader =  loader)
        data = cherrypy.request.json
        isPng = kwargs['type'] == 'png'
        print(data['keywords'])
        if (isPng):
            responseType = 'application/png'
        else:
            responseType = 'application/pdf'

        cherrypy.response.headers['Content-Type'] = responseType
        template = templateEnv.get_template('cv.html')
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
            return doc.write_png(target=None, stylesheets=[style])
        else:
            return doc.write_pdf(target=None, stylesheets=[style])
    # cv.exposed = True

cherrypy.quickstart(App())
