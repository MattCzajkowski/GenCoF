import shlex
import subprocess
import os
import sys
from tkinter import filedialog
from tkinter import *

##############################################################################
#
# Run - Closes window and opens GenCoF main
#
# App - Sets the window and grid of the app
#
## Functions within App:
## __init__ - Sets up the display of Join's main interface through
## buttons and labels
##
## MANDATORY - Sets up widgets for the mandatory options of App
##
## Check_Options - Checks the widgets used and creates a string of options
## that get inputted to terminal to run Join
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
        subprocess.call(['py', '-3', './GenCoF(Windows).py'])
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
            self.frame, text="Join", font="Times 20 bold", bg="white").grid(
                row=x,
                column=0,
                columnspan=10,
                padx=5,
                pady=(5, 5),
                sticky="we")
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
            text=
            "Input Files: Pick input files. Use control or shift click to select multiple files at a time",
            relief=FLAT,
            bg="white")
        self.label_filename.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_file_type = StringVar()
        self.var_file_type.set("Pick File Type")
        self.file_type = OptionMenu(self.frame, self.var_file_type, "FASTA",
                                    "FASTQ").grid(
                                        row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="File type as input ",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_out_file = StringVar()
        self.out_file = Entry(
            self.frame, textvariable=self.var_out_file, width=29).grid(
                row=x, column=0, padx=5, pady=5)
        self.var_out_file.set('Output Filename')
        Label(
            self.frame,
            text=
            "Output File: Will default to JOINED_OUTPUT with file type appended to end",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.run_button = Button(
            self.frame, text="Run Join", command=self.Check_Options)
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

        if (sys.platform == 'win32'):
            globstring = 'type '
        else:
            globstring = 'cat '
        errors = ''

        if (self.var_filename == ''):
            errors += "Enter Input Files\n"
        else:
            globstring += "'" + "' '".join(self.var_filename) + "'" + " "

        globstring += "> "

        if (self.var_out_file.get() == "Output Filename"
                or self.var_out_file.get() == ""):
            globstring += "JOINED_OUTPUT"
        else:
            globstring += self.var_out_file.get()

        if (self.var_file_type.get() == "Pick File Type"):
            errors += "Enter Input File type\n"
        elif (self.var_file_type.get() == "FASTA"):
            globstring += ".fasta"
        else:
            globstring += ".fastq"

        self.err_message.config(text="Running....", font="Times 18")
        self.update()
        if (errors == ''):
            cmd_line = shlex.split(globstring)
            p = subprocess.Popen(
                globstring,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
            output, error = p.communicate()
            if (error.decode('utf-8') == ''):
                self.err_message.config(
                    text="OUTPUT: \n" + output.decode('utf-8') + "Completed",
                    font="Times 18")
            else:
                self.err_message.config(
                    text='\n' + error.decode('utf-8'),
                    font="Times 18",
                    fg='dark red')
        else:
            self.err_message.config(
                text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")
        return

    def browse_file_input1(self):
        self.var_filename = filedialog.askopenfilenames(title='Choose a file')
        return

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return


if __name__ == "__main__":
    root = Tk()
    root.wm_title("Join")
    root.geometry('900x300')
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
