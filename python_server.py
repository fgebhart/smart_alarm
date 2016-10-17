import cgi

import xml_write
import xml_read

from datetime import datetime

import os.path
import settings


def create_page(setts, currentTime):
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
    ''' % {
        'currenTime': str(currentTime),
        'alarmTime': str(setts.alarm_time),
        'musicOrNewsImage': './left.png' if setts.content == 'music' else './right.png',
        'musicOrNewsValue': 'news' if setts.content == 'music' else 'music'
        }

    return html


def app(environ, start_response):
    # define settings
    #settings = namedtuple("settings", "alarm_active alarm_time content days individual_message text volume")
    setts = settings.Settings()

    # get current time
    currentTime = datetime.now().strftime('%H:%M:%S')

    # response for POST
    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
           fp=environ['wsgi.input'],
           environ=environ,
            keep_blank_values=True
        )

        setts.content = post.getvalue('musicOrNews')
        xml_write.create(currentTime, setts).writexml(open('data.xml', 'w'))

    path = str(environ['PATH_INFO'])

    if '.png' in path:
        # response for an image
        html = open("Images" + path, "rb").read()
        headers = [('Server', 'Apache'), ('Content-type', 'image/png')]
    else:
        # response for a normal html page

        # check if there is already a xml file, if not create one
        if not os.path.isfile('data.xml'):
            setts.fill_with_default_values()
            xml_write.create(currentTime, setts).writexml(open('data.xml', 'w'))

        # load settings from xml file
        try:
            xml_read.read_default('data.xml', setts)
        except:
            # file is not consistent
            setts.fill_with_default_values()
            xml_write.create(currentTime, setts).writexml(open('data.xml', 'w'))

        # create html page
        html = create_page(setts, currentTime)
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
    except KeyboardInterrupt:  # Strg + C
        httpd.server_close()
        print('Server Closed.')
    except:
        httpd.server_close()
        print('Error')
