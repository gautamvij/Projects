import pygame, random, sys, os
from pygame import mixer

mixer.init()

# returns corresponding music according to every map
def create_music(map_name):
        if map_name=='start':
                musicbg=mixer.Sound('./sounds/startup.ogg')
                musicbg.play(-1)
                return musicbg

        elif map_name=='./maps/village1.tmx':
                musicbg=mixer.Sound('./sounds/naturesounds.ogg')
                musicbg.play(-1)
                return musicbg

        elif map_name=='./maps/village2_out1.tmx':
                musicbg=mixer.Sound('./sounds/village2out.ogg')
                musicbg.play(-1)
                return musicbg

        elif map_name=='./maps/village2_inside.tmx':
                musicbg=mixer.Sound('./sounds/vil2in.ogg')
                musicbg.play(-1)
                return musicbg

        elif map_name=='./maps/ship.tmx':
                musicbg=mixer.Sound('./sounds/naturesounds1.ogg')
                musicbg.play(-1)
                return musicbg

        elif map_name == './maps/tunnel2_4.tmx':
                musicbg=mixer.Sound('./sounds/tunnel2_4.ogg')
                musicbg.play(-1)
                return musicbg
                
        elif map_name == './maps/tunnel3.tmx':
                musicbg=mixer.Sound('./sounds/DragonFlight.ogg')
                musicbg.play(-1)
                return musicbg
        
        elif map_name == './maps/mountain_top.tmx':
                musicbg=mixer.Sound('./sounds/mountain_top.ogg')
                musicbg.play(-1)
                return musicbg
        
        elif map_name == './maps/palace_final.tmx':
                musicbg=mixer.Sound('./sounds/battlefield.ogg')
                musicbg.play(-1)
                return musicbg

# creates sound object for given file and returns it
def create_soundfx(music_file):
        soundfx=mixer.Sound(music_file)
        soundfx.play()
        return soundfx

# stops the music
def stop_music():
        mixer.music.stop()

# stops the sound_object sound
def stop_soundfx(sound_object):
        sound_object.stop()

# creats another music object other than background music
def create_music_add(sound_file):
        musicfx=mixer.Sound(sound_file)
        musicfx.play(-1)
        return musicfx

# sets volume
def volume(sound_file,v):
        sound_file.set_volume(v)
