import pygame


def play_mp3_file(mp3_file):
    """using pygame lib in order to play mp3 sound files"""
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    print "now playing file: ", mp3_file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue



play_mp3_file("nachrichten_dlf_20160927_1030_edc3be5b.mp3")






