import tkinter
from tkinter import *
import subprocess
import os, sys

basedir = sys.executable
last_dir = basedir.rfind("/")
basedir = basedir[:last_dir]

os.chdir(basedir)

##############################################################################
# App - Sets
#


class App(Frame):
    def __init__(self, root):

        ##Start to Create the grid build of GUI##

        ##Sets up the frame of the window as well as adding a scrollbar
        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0, background="white")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(
            root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(
            (4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        ##Title of Deconseq Portion of GUI##
        self.file1_title = Label(
            self.frame, text="""GenCoF""", font="Times 24 bold",
            bg="white").grid(
                row=0,
                column=0,
                columnspan=10,
                padx=5,
                pady=(5, 5),
                sticky="we")

        ##Title of Deconseq Portion of GUI##
        self.file1_title = Label(
            self.frame,
            text="""Genomic Contamination Filtering Pipeline""",
            font="Times 16 bold",
            bg="white").grid(
                row=1,
                column=0,
                columnspan=10,
                padx=5,
                pady=(2, 2),
                sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=19,
            text="""STEP 1
(Filters DNA)""",
            font="Helvetica 15 bold",
            bg="white")
        b.grid(row=2, column=0, padx=5, pady=0, sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=23,
            text="""Alternate STEP 1 
(Filters DNA with more options)""",
            font="Helvetica 15 bold",
            bg="white")
        b.grid(row=2, column=1, padx=5, pady=0, sticky="we")

        b = Button(
            self.frame,
            height=3,
            width=19,
            text="OPEN SICKLE",
            command=self.Sickle)
        b.grid(row=3, column=0, padx=5, pady=(5, 5), sticky="we")

        b = Button(
            self.frame,
            height=3,
            width=19,
            text="OPEN PRINSEQ",
            command=self.Prinseq)
        b.grid(row=3, column=1, padx=5, pady=(5, 5), sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=75,
            bg="white",
            text=
            "Sickle Requirements: Requires C compiler and Python 3 module Tkinter",
            anchor="w")
        b.grid(row=4, column=0, sticky="w", columnspan=2)

        b = Label(
            self.frame,
            height=3,
            width=100,
            text=
            """Prinseq Requirements: Requires Perl modules(all Perl modules necessary come with Perl Installation)
and Python3 Tkinter""",
            anchor="w",
            justify=LEFT,
            bg="white")
        b.grid(row=5, column=0, sticky="w", columnspan=2)

        b = Label(
            self.frame,
            height=3,
            width=23,
            text="""Step 2
(Recommended for files over 1GB depending on computer speed)""",
            font="Helvetica 15 bold",
            bg="white")
        b.grid(row=6, column=0, padx=5, pady=0, columnspan=3, sticky="we")

        b = Button(
            self.frame,
            height=3,
            width=19,
            text="OPEN SPLIT",
            command=self.Split)
        b.grid(row=7, column=0, padx=5, pady=(5, 5), columnspan=3, sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=75,
            bg="white",
            text=
            "Split Requirements: Requires Perl and Python 3 module Tkinter",
            anchor="w")
        b.grid(row=8, column=0, sticky="w", columnspan=2)

        self.err = StringVar()
        self.err_message = Label(
            self.frame,
            text=self.err.get(),
            font="Helvetica 20",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.err_message.grid(
            row=9, column=0, padx=5, pady=0, columnspan=3, sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=35,
            text="""STEP 3 
(Create reference files for Bowtie2. Not necessary if database files already in bowtie2-2.3.4.1 folder)""",
            font="Helvetica 15 bold",
            bg="white")
        b.grid(row=10, column=0, padx=5, pady=0, columnspan=3, sticky="we")

        b = Button(
            self.frame,
            height=3,
            width=19,
            text="OPEN BOWTIE2 BUILD",
            command=self.Bowtie2_Build)
        b.grid(
            row=11, column=0, padx=5, pady=(5, 5), columnspan=3, sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=85,
            bg="white",
            text=
            """Bowtie2-Build Requirements: Requires Python 3 module Tkinter and GNU-like environment with GCC, GNU Make and other basics.
It should be possible to build Bowtie 2 on most vanilla Linux installations or on a Mac installation with Xcode installed""",
            anchor="w",
            justify=LEFT)
        b.grid(row=12, column=0, sticky="w", columnspan=2)

        b = Label(
            self.frame,
            height=3,
            width=35,
            text="""STEP 4 
(Outputs contaminated and contam-free data)""",
            font="Helvetica 15 bold",
            bg="white")
        b.grid(row=13, column=0, padx=5, pady=0, columnspan=3, sticky="we")

        b = Button(
            self.frame,
            height=3,
            width=19,
            text="OPEN BOWTIE2",
            command=self.Bowtie2)
        b.grid(
            row=14, column=0, padx=5, pady=(5, 5), columnspan=3, sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=85,
            bg="white",
            text=
            """Bowtie2 Requirements: Requires GNU-like environment with GCC, GNU Make and other basics.
It should be possible to build Bowtie 2 on most vanilla Linux installations or on a Mac installation with Xcode installed""",
            anchor="w",
            justify=LEFT)
        b.grid(row=15, column=0, sticky="w", columnspan=2)

        b = Label(
            self.frame,
            height=3,
            width=19,
            text="""STEP 4 
(If you used Split)""",
            font="Helvetica 15 bold",
            bg="white")
        b.grid(row=16, column=0, padx=5, pady=0, columnspan=3, sticky="we")

        b = Button(
            self.frame,
            height=3,
            width=19,
            text="OPEN JOIN",
            command=self.Join)
        b.grid(
            row=17, column=0, padx=5, pady=(5, 5), columnspan=3, sticky="we")

        b = Label(
            self.frame,
            height=3,
            width=75,
            bg="white",
            text=
            "Join Requirements: Requires cat executable and Python 3 module Tkinter",
            anchor="w")
        b.grid(row=18, column=0, sticky="w", columnspan=2)

    def onFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return

    def error(self):
        self.err_message.config(
            text='\n**Graphical User Interface file not found**',
            fg='dark red')
        return

    def Sickle(self):
        if ('sickle-gui.py' in os.listdir('./GenCoF-master/Sickle/')):
            root.destroy()
            subprocess.call(
                ['chmod', '+x', './GenCoF-master/Sickle/sickle-master/sickle'])
            subprocess.call(
                ['python3', './GenCoF-master/Sickle/sickle-gui.py'])
        else:
            self.error()
        return

    def Bowtie2_Build(self):
        if ('bowtie2-build-gui.py' in os.listdir('./GenCoF-master/Bowtie2/')):
            root.destroy()
            subprocess.call([
                'chmod', '+x',
                './GenCoF-master/Bowtie2/bowtie2-2.3.4.1/bowtie2-build'
            ])
            subprocess.call(
                ['python3', './GenCoF-master/Bowtie2/bowtie2-build-gui.py'])
        else:
            self.error()
        return

    def Bowtie2(self):
        if ('bowtie2-gui.py' in os.listdir('./GenCoF-master/Bowtie2/')):
            root.destroy()
            subprocess.call([
                'chmod', '+x',
                './GenCoF-master/Bowtie2/bowtie2-2.3.4.1/bowtie2'
            ])
            subprocess.call(
                ['python3', './GenCoF-master/Bowtie2/bowtie2-gui.py'])
        else:
            self.error()
        return

    def Prinseq(self):
        if ('prinseq-gui.py' in os.listdir('./GenCoF-master/Prinseq/')):
            root.destroy()
            subprocess.call([
                'chmod', '+x',
                './GenCoF-master/Prinseq/prinseq-lite-0.20.4/prinseq-lite.pl'
            ])
            subprocess.call(
                ['python3', './GenCoF-master/Prinseq/prinseq-gui.py'])
        else:
            self.error()
        return

    def Split(self):
        if ('split-gui.py' in os.listdir('./GenCoF-master/Split/')):
            root.destroy()
            subprocess.call([
                'chmod', '+x',
                './GenCoF-master/Split/Split_files/fastq-splitter.pl'
            ])
            subprocess.call([
                'chmod', '+x',
                './GenCoF-master/Split/Split_files/fasta-splitter.pl'
            ])
            subprocess.call(['python3', './GenCoF-master/Split/split-gui.py'])
        else:
            self.error()
        return

    def Join(self):
        if ('join-gui.py' in os.listdir('./GenCoF-master/Join/')):
            root.destroy()
            subprocess.call(['python3', './GenCoF-master/Join/join-gui.py'])
        else:
            self.error()
        return


if __name__ == "__main__":
    ##Start of App
    ##Creates Window and goes to the Mainloop of the class and creates the App
    root = Tk()
    root.wm_title("GenCoF")
    root.geometry('950x550')
    app = App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
