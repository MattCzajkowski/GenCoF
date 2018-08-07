import shlex
import subprocess
import os
import sys
from tkinter import filedialog
from tkinter import *

##############################################################################

#__author__ = "Matt Czajkowski" 
#__copyright__ = "Copyright 2018, Evolve Biosystems"
#__credits__ = ["Matt Czajkowski", "Daniel Vance", "Steve Frese", "Giorgio Casaburi"]
#__license__ = "GPL v3.0"
#__version__ = "1.0.0"
#__maintainer__ = "Matt Czajkowski"
#__email__ = "mczajkowski@evolvebiosystems.com"

##############################################################################

##############################################################################
# 
# Run - Closes window and opens GenCoF main
#
# App - Sets the window and grid of the app
#
## Functions within App:
## __init__ - Sets up the display of Bowtie-build's main interface through
## buttons and labels
##
## MANDATORY - Sets up widgets for the mandatory options of App
##
## Check_Options - Checks the widgets used and creates a string of options
## that get inputted to terminal to run Bowtie2-build
##
## browse_file_input1 - Lets user choose a file and puts the file path in a
## variable
##
## onFrameConfigure - Creates a scrollbar 
# 
# __name__ - Sets up base directory, builds App and sets up window size
#
##############################################################################

def Run():
    root.destroy()
    if (sys.platform == 'linux'):
        subprocess.call(['chmod', '+x', './GenCoF(Linux)'])
        subprocess.call(['./GenCoF(Linux)'])
    if (sys.platform == 'darwin'):
        subprocess.call(['chmod', '+x', './GenCoF(Mac)'])
        subprocess.call(['./GenCoF(Mac)'])
    if (sys.platform == 'win32'):
        subprocess.call(['py', '-3', './GenCoF(Windows)'])
    return


class App(Frame):
    def __init__(self, root):
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

        self.MANDATORY()
        return

    def MANDATORY(self):
        x = 0
        self.run_butt = Button(self.frame, text="BACK", command=Run)
        self.run_butt.grid(row=x, column=0, padx=5, pady=5, sticky="w")
        x += 1

        self.file1_title = Label(
            self.frame, text="Bowtie2 Build", font="Times 20 bold",
            bg="white").grid(
                row=x,
                column=0,
                columnspan=10,
                padx=5,
                pady=(5, 5),
                sticky="we")
        x += 1

        self.fill_mandat = Label(
            self.frame,
            text=
            "Citation: B. Langmead, C. Trapnell, M. Pop, S.L. Salzberg: Ultrafast and memory-efficient alignment of short DNA sequences to the human genome Genome Biol., 10 (2009), p. R25",
            font="Times 10 bold",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.fill_mandat = Label(
            self.frame,
            text=
            """Before running it is recommended to look at https://support.illumina.com/sequencing/sequencing_software/igenome.html
for reference files to download, as creating reference files from scratch can be time intensive.""",
            font="Times 16",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_filename = ''
        self.browse_file = Button(
            self.frame,
            text="Browse",
            command=self.browse_file_input1,
            width=15)
        self.browse_file.grid(row=x, column=0, padx=5, pady=5)
        self.label_filename = Label(
            self.frame,
            text="Input File: Pick input file to use as reference.",
            relief=FLAT,
            bg="white")
        self.label_filename.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_out_file = StringVar()
        self.out_file = Entry(
            self.frame, textvariable=self.var_out_file, width=29).grid(
                row=x, column=0, padx=5, pady=5)
        self.var_out_file.set('Output Files Basename')
        Label(
            self.frame,
            text=
            "Output File: Will default to hg with file type appended to end",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.run_button = Button(
            self.frame, text="Run Bowtie2 Build", command=self.Check_Options)
        self.run_button.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.err = StringVar()
        self.err_message = Label(
            self.frame,
            text=self.err.get(),
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.err_message.grid(
            row=x, column=0, columnspan=5, padx=5, sticky="w")

        return

    def Check_Options(self):

        globstring = "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/bowtie2-build "
        errors = ''
        if (self.var_filename == ''):
            errors += "Enter Input Files\n"
        else:
            globstring += self.var_filename + " "

        if (self.var_out_file.get() == "Output Filename"
                or self.var_out_file.get() == ""):
            globstring += "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/" + "hg"
        else:
            globstring += "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/" + self.var_out_file.get(
            )

        if (errors == ''):
            cmd_line = shlex.split(globstring)
            if ('bowtie2-build-l' in os.listdir(
                    './GenCoF-master/Bowtie2/bowtie2-2.3.4.1/')):
                self.err_message.config(text="Running....", font="Times 18")
                self.update()
                p = subprocess.Popen(
                    cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = p.communicate()
                if (error.decode('utf-8') == ''):
                    self.err_message.config(
                        text="OUTPUT: \n" + output.decode('utf-8'),
                        font="Times 18")
                else:
                    self.err_message.config(
                        text='\n' + error.decode('utf-8'),
                        font="Times 18",
                        fg='dark red')
            elif ('Makefile' in os.listdir(
                    './GenCoF-master/Bowtie2/bowtie2-2.3.4.1/')):
                self.err_message.config(text="Compiling....", font="Times 18")
                self.update()
                subprocess.call(
                    ["make", "-C", "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/"])
                self.err_message.config(text="Running....", font="Times 18")
                self.update()
                p = subprocess.Popen(
                    cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result, error = p.communicate()
                if (error.decode('utf-8') == ''):
                    self.err_message.config(
                        text="\n" + result.decode('utf-8'),
                        font="Times 18")
                else:
                    self.err_message.config(
                        text='\n' + error.decode('utf-8'),
                        font="Times 18")
            else:
                self.err_message.config(
                    text="ERRORS: \n Makefile not in correct directory",
                    font="Times 18")
        else:
            self.err_message.config(
                text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")

        return

    def browse_file_input1(self):
        self.var_filename = filedialog.askopenfilename()
        return

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return


if __name__ == "__main__":
    root = Tk()
    root.wm_title("BOWTIE2 BUILD")
    root.geometry('900x300')
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
