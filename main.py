#!/usr/bin/env python3

import cherrypy
import weasyprint

class Pdf(object):
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        doc = weasyprint.HTML(base_url=".", string = """
        <!doctype html>
        <html>
          <head>
        <title>CV</title>
          </head>
          <body>
            <div class="left-pane">
              <img class="pic" src="foo.jpg" />
              <div class="keywords">
                <ul>
                  <li>Web Backend</li>
                  <li>Web Frontend</li>
                  <li>DevOps</li>
                  <li>Software Project Management</li>
                </ul>
              </div>
            </div>
            <div class="right-pane">
              <h1 class="name">Daniel Landau</h1>
              <h2 class="title">Software Developer</h2>
              <p class="intro-text">I am a builder and problem solver. The solution will get done in whatever way is required from Haskell through Java to machine language and beyond. I understand the language of business and can ask the right questions at the right time to arrive at the best possible outcome. I am a generalist with strong experience in full stack web development.</p>
              <div class="experience">
                <h3>Experience</h3>
                <dl>
                <dt>Software Developer</dt>
                <dd>Futurice Oy 2014-Present</dd>
                <span>—</span>
                <dt>High Performance Analysis</dt>
                <dd>Cray Inc 2013-2014</dd>
                <span>—</span>
                <dt>Research Assistant</dt>
                <dd>University of Helsinki 2011-2012</dd>
                <span>—</span>
                <dt>Intern</dt>
                <dd>CSC 2011, FMI 2009-2011</dd>
                </dl>
              </div>
              <div class="education">
                <h3>Education</h3>
                <dl>
                <dt>University of Helsinki</dt>
                <dd>M.Sc., Theoretical Physics</dd>
                <dd>2008-2013</dd>
                </dl>
              </div>
              <div class="social">
                <span class="email">daniel.landau@futurice.com</span>
                <span class="twitter">@Daniel_Landau</span>
                <span>fi.linkedin.com/in/landaudaniel</span>
              </div>
            </div>
          </body>
        </html>""")
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
        return doc.write_png(target=None, stylesheets=[style])
    index.exposed = True

cherrypy.quickstart(Pdf())
