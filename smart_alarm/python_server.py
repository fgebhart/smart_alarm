import cgi
import sys
import os.path

import base64 # for decoding mp3 data from webserver

# important for apache web server:
project_path = os.environ['smart_alarm_path']
if project_path not in sys.path:
    sys.path.append(project_path)
os.chdir(project_path)

from smart_alarm.smart_alarm.modules.xml_data import Xml_data


# import xml class
xml_data = Xml_data(str(project_path) + '/data.xml')

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.xml': 'text/xml',
              '.js': 'application/javascript',
              '.png': 'image/png'
             }


def application(environ, start_response):
    # response for POST
    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
           fp=environ['wsgi.input'],
           environ=environ,
           keep_blank_values=False
        )

        uploaded_mp3_file = {}
        for s in post:
            if 'uploadMp3File' in s:
                fieldName = s[s.find('[')+1:s.find(']')]
                uploaded_mp3_file[fieldName] = post.getvalue(s)
            elif s == 'deleteMp3File':
                os.remove('./music/' + post.getvalue(s))
                xml_data.readFileNamesInMusicDirectory()
            else:
                try:
                    xml_data.changeValue(s, post.getvalue(s))
                    print s + ' changed to ' + post.getvalue(s)
                except:
                    print 'Error: Couldn\'t change xml entry ' + s + ' to ' + post.getvalue(s)

        if uploaded_mp3_file:
            mp3_data_base64 = uploaded_mp3_file['fileData'][uploaded_mp3_file['fileData'].find('base64,')+7:]
            # mp3_data = decode_base64(mp3_data_base64)
            f = open('./music/' + uploaded_mp3_file['name'], 'w')
            f.write(base64.b64decode(mp3_data_base64))
            f.close()
            xml_data.readFileNamesInMusicDirectory()

    path = environ['PATH_INFO']
    if path != '/data.xml':
        path = './web' + path
    else:
        path = '.' + path

    if os.path.exists(path):
        if path == './web/':
            path = './web/index.html'
        h = open(path, 'rb')
        content = h.read()
        h.close()

        headers = [('content-type', content_type(path))]
        start_response('200 OK', headers)
        return [content]
    else:
        return show_404_app(environ, start_response, path)




def content_type(path):
    """Return a guess at the mime type for this path
    based on the file extension"""

    name, ext = os.path.splitext(path)

    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"

def show_404_app(environ, start_response, path):
    start_response('404 Not Found', [('content-type','text/html')])
    return ["""<html><h1>""" + path + """ not Found</h1><p>
               That page is unknown. Return to
               the <a href="/">alarm clock</a>.</p>
               </html>""", ]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import webbrowser

    httpd = make_server('', 8090, application)
    print('Serving on port 8090...')

    url = "http://127.0.0.1:8090"
    webbrowser.open(url)

    print(os.getcwd())
    try:
        while True:
            print('Server request.')
            httpd.handle_request()
    except KeyboardInterrupt:  # Strg + C
        httpd.server_close()
        print('Server Closed.')
    except:
        httpd.server_close()
        print('Error')
