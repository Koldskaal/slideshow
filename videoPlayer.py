import os
os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')

import vlc
import sys
import time

from os.path import basename, expanduser, isfile, join as joined

import tkinter as tk

playing = set([1,2,3,4])

_isMacOS   = sys.platform.startswith('darwin')
_isWindows = sys.platform.startswith('win')
_isLinux = sys.platform.startswith('linux')


# time.sleep(5) #Give it time to get going
# while True:
#    state = player.get_state()
#    if state not in playing:
#        break

class Player(tk.Frame):
    """The main window has to deal with events.
    """
    _geometry = ''
    _stopped  = None

    def __init__(self, parent, title=None, onVideoEnd=None):
        tk.Frame.__init__(self, parent)

        self.parent = parent  # == root
        self.parent.title(title or "tkVLCplayer")

        self.callback = onVideoEnd
        # first, top panel shows video
        # self.videopanel = tk.Frame(self.parent)
        # self.videopanel.pack(side="top", fill="both", expand=True)
        # self.videopanel.wm_geometry = self.parent.geometry()
        # VLC player
        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()
        self.player.audio_set_mute(True)
        self.parent.update()

    def OnClose(self, *unused):
        """Closes the window and quit.
        """
        self.parent.quit()  # stops mainloop
        self.parent.destroy()  # this is necessary on Windows to avoid
        # ... Fatal Python Error: PyEval_RestoreThread: NULL tstate
        sys.exit(0)

    def play(self, video):
        # video = expanduser(video)
        if isfile(video):  # Creation
            m = self.Instance.media_new(str(video))  # Path, unicode
            self.player.set_media(m)
            self.parent.title("tkVLCplayer - %s" % (basename(video),))

            # set the window id where to render VLC's video output
            h = self.winfo_id()  # .winfo_visualid()?
            if _isWindows:
                self.player.set_hwnd(h)
            elif _isMacOS:
                # XXX 1) using the videopanel.winfo_id() handle
                # causes the video to play in the entire panel on
                # macOS, covering the buttons, sliders, etc.
                # XXX 2) .winfo_id() to return NSView on macOS?
                v = _GetNSView(h)
                if v:
                    self.player.set_nsobject(v)
                else:
                    self.player.set_xwindow(h)  # plays audio, no video
            else:
                self.player.set_xwindow(h)  # fails on Windows
            # FIXME: this should be made cross-platform
            if self.player.play():  # == -1
                print("Unable to play the video.")


    def check_video_end(self):

       state = self.player.get_state()
       if state not in playing:
           self.after(5 * 1000, self.check_video_end)
       else:
           if self.callback:
               self.callback()

if __name__ == "__main__":
    # Create a tk.App() to handle the windowing event loop
    root = tk.Tk()
    player = Player(root)
    player.play('.\\maranata.mp4')
    player.pack(fill="both", expand=True)
    root.protocol("WM_DELETE_WINDOW", player.OnClose)  # XXX unnecessary (on macOS)
    root.mainloop()
