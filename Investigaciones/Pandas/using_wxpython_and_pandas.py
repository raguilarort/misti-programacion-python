import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx.lib.scrolledpanel as scrolled
import pandas as pd
import matplotlib.pyplot as plt

class GraphPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, fig):
        super().__init__(parent)
        self.figure = fig
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
        self.SetupScrolling()

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        ax = df.plot()
        fig = ax.figure

        super().__init__(*args, **kw)
        panel = GraphPanel(self, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

# Función main
def main():
    
    app = wx.App(False)
    frame = MainFrame(None, title="Pandas Graph in wxPython")
    frame.Show()
    app.MainLoop()

# Se invoca funcion main()
if __name__ == '__main__':
    main()