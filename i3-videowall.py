#!/usr/bin/env python
#

import i3
import shlex
import os

from subprocess import Popen
from time import sleep
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

class player_window(object):
    def __init__(self, window):
        self.window=window
        self.id=window['id']
        self.height=window['rect']['height']
        self.width=window['rect']['width']
        self.area=self.width*self.height
    
def find_player_to_split():
    """
    Find the largest of the MPlayer windows and focus on it and decide
    to split either horizontally or vertically
    """
    windows = i3.filter(name="MPlayer")
    if len(windows)>0:
        biggest = player_window(windows[0])
        for w in windows:
            w = player_window(w)
            if w.area>biggest.area:
                biggest = w

        return biggest
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
            w = find_player_to_split()
            if w:
                print "Found a window %d to split (%dx%d)" % (w.id, w.width, w.height)
                print "focusing: %s " % (i3.focus(con_id=w.id))
                if w.width>w.height:
                    print "horizontal"
                    i3.split("h")
                else:
                    print "vertical"
                    i3.split("v")

#                print "refocusing: %s " % (i3.focus(id=w.id))
                state = i3.filter(id=w.id)
                print "State of window is: %s" % (state)
            else:
                print "No window to split"

            player = Popen(cmd, stdout=dev_null, stderr=dev_null)
            playing_videos.append(player)
            print "playing_videos now: %d, %s" % (len(playing_videos), playing_videos)
            sleep(1)

        print "starting poll cycle"
        for p in playing_videos:
            x=p.poll()
            print "poll of %s gave %s" % (p, x)
            if x is not None:
                playing_videos.remove(p)
            sleep(10)
        
        

    print "No videos left"

















