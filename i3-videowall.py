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

parser.add_argument('files', metavar='FILES_TO_PLAY', nargs='+', help='File to play')
parser.add_argument('-n', default=2, help="Maximum to play at one time")

if __name__ == '__main__':
    args = parser.parse_args()

    # prepare
    to_play = args.files
    video_commands = shlex.split(MPLAYER_CMD)
    dev_null = os.open("/dev/null", os.O_WRONLY)

    i3.workspace('videowall')
    i3.layout('default')

    playing_videos = []
    while len(to_play)>0:

        # start playing
        while len(playing_videos)<args.n and len(to_play)>0:
            video=to_play.pop()
            print "Going to play %s" % (video)
            cmd = list(video_commands)
            cmd.append(video)
            print "cmd=%s" % (cmd)
            i3.workspace('videowall')

            player = Popen(cmd, stdout=dev_null, stderr=dev_null)
            playing_videos.append(player)

        print "starting poll cycle"
        for p in playing_videos:
            x=p.poll()
            print "poll of %s gave %s" % (p, x)
            if x is not None:
                playing_videos.remove(p)
            sleep(10)
        
        

    print "No videos left"

















