#!/usr/bin/env python
#

import i3
import shlex
import os

from subprocess import Popen
from time import sleep
from random import choice
from argparse import ArgumentParser

MPLAYER_CMD="/usr/bin/mplayer -zoom -noborder -nosound"

#
# Command line options
#
parser=ArgumentParser(description='Play a wall of video in i3-wm.',
                      epilog="""This script creates a video-wall on a new workspace of videos.
                      It's a good way to stress your processor""")

parser.add_argument('files', metavar='VIDEO', nargs='+', help='File to play')
parser.add_argument('-n', type=int, default=2, help="Maximum to play at one time")
parser.add_argument('--split', '-s', default="biggest", help="Which window to split when starting a new one")

class rect(object):
    """
    A simple container for rectangles
    """
    def __init__(self, rect_hash):
        self.__dict__.update(rect_hash)
        self.area = self.width*self.height

    def __str__(self):
        return "%dx%d" % (self.width, self.height)

    def is_wider(self):
        if self.width>self.height:
            return True
        else:
            return False

class player_window(object):

                
    def __init__(self, window):
        self.window=window
        # slurp hash into object
        self.__dict__.update(window)
        # calculate area
        self.container = rect(self.rect)
        self.player = rect(self.window_rect)

    def __str__(self):
        return "Window ID:%d %s (player %s)" % (self.id,
                                                self.container,
                                                self.player)
        
def find_player_to_split(method="biggest"):
    """
    Find the largest of the MPlayer windows and focus on it and decide
    to split either horizontally or vertically
    """
    windows = i3.filter(name="MPlayer")
    if len(windows)>0:
        window_list = [player_window(w) for w in windows]
        if method=="biggest":
            return max(window_list,key=lambda w: w.player.area)
        elif method=="random":
            return choice(window_list)
            
    else:
        return None

if __name__ == '__main__':
    args = parser.parse_args()

    # prepare
    to_play = args.files
    max_play = args.n
    video_commands = shlex.split(MPLAYER_CMD)
    dev_null = os.open("/dev/null", os.O_WRONLY)

    i3.workspace('videowall')
    i3.layout('default')

    print "max is %d" % (max_play)
    playing_videos = []
    while len(to_play)>0:

        # start playing
        while len(playing_videos)<max_play and len(to_play)>0:
            video=to_play.pop()
            print "Going to play %s" % (video)
            cmd = list(video_commands)
            cmd.append(video)
            print "cmd=%s" % (cmd)

            i3.workspace('videowall')
            w = find_player_to_split(args.split)
            if w:
                print "Found: %s" % (w)
                print "focusing: %s " % (i3.focus(con_id=w.id))
                if w.container.is_wider():
                    i3.split("h")
                else:
                    i3.split("v")

            else:
                print "No window to split"

            player = Popen(cmd, stdout=dev_null, stderr=dev_null)
            playing_videos.append(player)
            print "playing_videos now: %d, %s" % (len(playing_videos), playing_videos)
            sleep(0.5)

        print "starting poll cycle"
        for p in playing_videos:
            x=p.poll()
            print "poll of %s gave %s" % (p, x)
            if x is not None:
                playing_videos.remove(p)
            sleep(10)
        
        

    print "No videos left"

















