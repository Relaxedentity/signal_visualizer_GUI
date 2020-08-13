import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from PIL import Image, ImageTk
import tkinter as tk
from matplotlib.backends.backend_agg import FigureCanvasAgg
from tkinter import filedialog

class App(object):
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title('DRM Visualization')
        
        menubar = tk.Menu(self.root)
        menubar.add_command(label="Open", command=self.open_file)
        self.root.config(menu=menubar)
        
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.imoncan = self.canvas.create_image(0,0,anchor='nw')
        self.canvas.grid(row=0, column=0)
        
        self.drpcanvas = tk.Label(self.root)
        self.drpcanvas.grid(row=0, column=1)
        
        self.frame_commands = tk.Frame(self.root, width=500, height=250, bg='grey')
        self.frame_commands.grid(row=1, column=0, columnspan=2)
        
        self.root.mainloop()
        
    def open_file(self):
        filename = filedialog.askopenfilename(
                   initialdir=os.path.dirname(os.path.abspath(__file__)), 
                   title = "Select file",
                   filetypes = [('numpy files', '.npy')],
                   )
        
        self.data = np.load(filename)
        self.shape = self.data.shape
        
        self.rx, self.ry = self.shape[0], self.shape[1]
        if self.rx<=self.ry:
            self.ymax = 500
            self.xmax = int(500/self.ry*self.rx)
        else:
            self.xmax = 500
            self.ymax = int(500/self.rx*self.ry)
        
        self.scalePhi = tk.Scale(self.frame_commands, 
                                 from_=0, 
                                 to_=self.shape[2]-1, 
                                 resolution=1, 
                                 command=self.update_phi, 
                                 orient='horizontal', 
                                 width=20, length=200,
                                 label='Azimuth')
        
        self.scalePhi.grid(row=0, column=0)
        self.scalePhi.set(0)
        
        self.scaleThe = tk.Scale(self.frame_commands, 
                                 from_=0,
                                 to_=self.shape[3]-1, 
                                 resolution=1, 
                                 command=self.update_theta, 
                                 orient='horizontal', 
                                 width=20, length=200,
                                 label='Elevation')
        
        self.scaleThe.grid(row=1, column=0)
        self.scalePhi.set(0)
        
        self.micrograph = self.data[...,0,0]
        self.canvas.bind('<Motion>', self.motion)
        self.update_micrograph()

    def update_phi(self, new_phi):
        self.current_phi = int(new_phi)
        self.micrograph = self.data[...,self.current_phi, self.current_the]
        self.update_micrograph()
  
    def update_theta(self, new_theta):
        self.current_the = int(new_theta)        
        self.micrograph = self.data[...,self.current_phi, self.current_the]
        self.update_micrograph()

    def update_micrograph(self):
        self.micro = Image.fromarray(self.micrograph)
        self.micro = self.micro.resize((self.xmax, self.ymax))
        self.micro = ImageTk.PhotoImage(self.micro)
        self.canvas.configure(width=self.xmax, height=self.ymax)
        self.canvas.itemconfig(self.imoncan, image=self.micro)
    
    def motion(self, event):
        '''
        Updates the DRP signal based on position of the mouse cursor.
        - event.x and event.y are the coordinates of the mouse cursor
        '''
        x, y = (event.x, event.y)
        
        # Rescale and clip
        x = np.clip(
            np.floor(x/self.xmax*self.rx).astype('int'), 
            a_min=0, a_max=self.shape[0]-1)
        y = np.clip(
            np.floor(y/self.ymax*self.ry).astype('int'), 
            a_min=0, a_max=self.shape[1]-1)
        
        # FOR SOME REASON, X AND Y MUST BE INVERTED (y,x) inst. of (x,y) !!
        drp = self.data[y, x].reshape((self.shape[2], self.shape[3])).T
        
        # Circular plot
        fig = self.circular_plot(drp)
        
        # Update image in the GUI
        drpim = FigureCanvasAgg(fig)
        s, (width, height) = drpim.print_to_buffer()
        drpim = np.frombuffer(s, np.uint8).reshape((height, width, 4))
        drpim = Image.fromarray(drpim, mode='RGBA')
        drpim = ImageTk.PhotoImage(drpim)
        self.drpcanvas.configure(image=drpim)
        self.drpcanvas.image = drpim
    
    def circular_plot(self, drp):
        '''Wraps the signal in a circular plot'''
        s0, s1 = self.shape[2], self.shape[3]        
        fig, ax = plt.subplots(figsize=(3,3))
        u = np.arange(0, 2*pi*(1+1/s1), 2*pi/s1)
        a = pi/2*0/90
        b = pi/2*65/90
        v = np.arange(a, b, (b-a)/(s0+1))
        x = np.outer(np.cos(u),np.cos(v))
        y = np.outer(np.sin(u),np.cos(v))
        ax.pcolormesh(x, y, drp, cmap=plt.cm.jet)
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.axis('off')
        plt.close()
        return fig

if __name__=='__main__':
    app = App()

