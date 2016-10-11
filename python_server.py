
import cgi

from save_xml_file import create_xml
from read_xml import read_xml_file_namedtuple

from datetime import datetime

import os.path



def create_page(settings, currentTime):
    # html template
    html = '''
    <html>
        <head>
            <title>Fabians und Sebastian toller Wecker</title>
        </head>
        <body>
            <h1>Wecker</h1>

            Current Time: %(currenTime)s <br>

            Alarm Time: %(alarmTime)s <br>

            <form method='post' action="">
                <input type="hidden" name="musicOrNews" value="%(musicOrNewsValue)s">
                Music <input type="image" src="%(musicOrNewsImage)s" name="change_content" value="testlal"> News <br>
            </form>
        </bod>
    </html>
    '''% {
        'currenTime': str(currentTime),
        'alarmTime': str(settings.alarmtime),
        'musicOrNewsImage': './left.png' if settings.content == 'music' else './right.png',
        'musicOrNewsValue': 'news' if settings.content == 'music' else 'music'
        }

    return html

def app(environ, start_response):

    # get current time
    currentTime = datetime.now().strftime('%H:%M:%S')

    # response for POST
    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
           fp=environ['wsgi.input'],
           environ=environ,
            keep_blank_values=True
        )

        content = post.getvalue('musicOrNews')

        create_xml(currentTime, "13:00", content, "monday tuesday").writexml(open('data.xml', 'w'))

    path = str(environ['PATH_INFO'])

    if '.png' in path:
        # response for an image
        html = open("Images" + path, "rb").read()
        headers = [('Server', 'Apache'), ('Content-type', 'image/png')]
    else:
        # response for a normal html page

        # check if there is already a xml file, if not create one
        if not os.path.isfile('data.xml'):
            create_xml(currentTime, "13:00", "news", "monday tuesday").writexml(open('data.xml', 'w'))

        # load settings from xml file
        settings = read_xml_file_namedtuple('data.xml')

        # create html page
        html = create_page(settings, currentTime)
        headers = [('Server', 'Apache'), ('Content-type', 'text/html')]

    start_response('200 OK', headers)

    return [html]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8090, app)
    print('Serving on port 8090...')
    print(os.getcwd())
    try:
        while True:
            print('Server request.')
            httpd.handle_request()
    except KeyboardInterrupt: # Strg + C
        httpd.server_close()
        print('Server Closed.')
    except:
        httpd.server_close()
        print('Error')
