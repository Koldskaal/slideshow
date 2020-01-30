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
Instance = vlc.Instance()

if len(sys.argv) == 2:
    curr_dir = sys.argv[1]
else:
    curr_dir = '.'

mp4list = []

for root, dirs, files in os.walk(curr_dir):
    for f in files:
        if f.endswith(".mp4"):
            img_path = os.path.join(root, f)
            mp4list.append(img_path)

player = Instance.media_player_new()
player.set_mrl(mp4list[0])


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

    def __init__(self, parent, title=None, video='', onVideoEnd=None):
        tk.Frame.__init__(self, parent)

        self.parent = parent  # == root
        self.parent.title(title or "tkVLCplayer")


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

        self.parent.update()
        # self._previouscreen = self.parent.geometry()

        self.Play(expanduser(video))

        # self.OnFullScreen()

    def OnClose(self, *unused):
        """Closes the window and quit.
        """
        self.parent.quit()  # stops mainloop
        self.parent.destroy()  # this is necessary on Windows to avoid
        # ... Fatal Python Error: PyEval_RestoreThread: NULL tstate
        sys.exit(0)

    def OnFullScreen(self, *unused):
        """Toggle full screen, macOS only.
        """
        # <https://www.Tcl.tk/man/tcl8.6/tkCmd/wm.htm#M10>
        f = not self.parent.attributes("-fullscreen")  # or .wm_attributes
        if f:
            self._previouscreen = self.parent.geometry()
            self.parent.attributes("-fullscreen", f)  # or .wm_attributes
            self.parent.bind("<Escape>", self.OnFullScreen)
        else:
            self.parent.attributes("-fullscreen", f)  # or .wm_attributes
            self.parent.geometry(self._previouscreen)
            self.parent.unbind("<Escape>")

    def OnMute(self, *unused):
        """Mute/Unmute audio.
        """
        # audio un/mute may be unreliable, see vlc.py docs.
        self.volMuted = m = not self.volMuted  # self.player.audio_get_mute()
        self.player.audio_set_mute(m)
        u = "Unmute" if m else "Mute"
        self.fileMenu.entryconfig(self.muteIndex, label=u)
        self.muteButton.config(text=u)
        # update the volume slider text
        self.OnVolume()

    def OnOpen(self, *unused):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.OnStop()
        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a video".
        video = askopenfilename(initialdir = Path(expanduser("~")),
                                title = "Choose a video",
                                filetypes = (("all files", "*.*"),
                                             ("mp4 files", "*.mp4"),
                                             ("mov files", "*.mov")))
        self.Play(video)

    def Play(self, video):
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
            self.OnPlay()

    def OnPlay(self, *unused):
        """Play video, if none is loaded, open the dialog window.
        """
        # if there's no video to play or playing,
        # open a tk.FileDialog to select a file
        if not self.player.get_media():
            if self.video:
                self._Play(expanduser(self.video))
                self.video = ''
            else:
                self.OnOpen()
        # Try to play, if this fails display an error message
        elif self.player.play():  # == -1
            self.showError("Unable to play the video.")
        else:
            # set volume slider to audio level
            vol = self.player.audio_get_volume()
            if vol > 0:
                self.volVar.set(vol)
                self.volSlider.set(vol)

    def CheckVideoEnd(self):

       state = player.get_state()
       if state not in playing:
           self.after(CheckVideoEnd, 5 * 1000)
       else:
           if onVideoEnd:
               self.callback()

    def showError(self, message):
        """Display a simple error dialog.
        """
        self.OnStop()
        showerror(self.parent.title(), message)

if __name__ == "__main__":
    # Create a tk.App() to handle the windowing event loop
    root = tk.Tk()
    player = Player(root, video=mp4list[0])
    root.protocol("WM_DELETE_WINDOW", player.OnClose)  # XXX unnecessary (on macOS)
    root.mainloop()
