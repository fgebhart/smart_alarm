import urllib2
import pygame


# dlf news:             http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml
# actual mp3 news:      http://podcast-mp3.dradio.de/podcast/2016/09/27/nachrichten_dlf_20160927_1030_edc3be5b.mp3
# sample sound file:    http://static1.grsites.com/archive/sounds/cartoon/cartoon001.mp3

url = "http://podcast-mp3.dradio.de/podcast/2016/09/27/nachrichten_dlf_20160927_1030_edc3be5b.mp3"

file_name = url.split('/')[-1]
u = urllib2.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()

print   "File successfully downloaded ... now playing it"

pygame.mixer.init()
pygame.mixer.music.load(file_name)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue