import signal
import swaramBase
import mainWindow

swaramBaseConfigure = swaramBase.swaramBase()

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)

mainWindow.mainWindow()
