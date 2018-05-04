import shlex, subprocess, os, sys
from tkinter import filedialog
from tkinter import *


#Specifications: Requires Python 3 module Tkinter
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

        ##Go To Build Mandatory Section
        self.MANDATORY()
        return

    def MANDATORY(self):

        x = 0  #current row for grid

        ##Returns to run where you can select another module of the GUI
        self.run_butt = Button(self.frame, text="BACK", command=Run)
        self.run_butt.grid(row=x, column=0, padx=5, pady=5, sticky="w")
        x += 1

        ##Title of Bowtie2-Build Portion of GUI##
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

        ##Citation for Bowtie2
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
for reference files to download as creating reference files from scratch can be time intensive.""",
            font="Times 16",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        ##Input File Section
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

        ##Output Filename Section
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

        ##Run Button which goes to function: Check_Options when clicked
        self.run_button = Button(
            self.frame, text="Run Bowtie2 Build", command=self.Check_Options)
        self.run_button.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Error Output To Screen Label
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

        ##Looks at the options that have been checked off and creates a string##
        ##Set the start of the string
        globstring = "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/bowtie2-build "
        ##Set errors to nothing
        ##If errors present add on string of errors
        errors = ''

        if (self.var_filename == ''):  # Get Input Filename
            errors += "Enter Input Files\n"
        else:
            globstring += self.var_filename + " "

        if (self.var_out_file.get() == "Output Filename"
                or self.var_out_file.get() == ""):
            globstring += "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/" + "hg"
        else:
            globstring += "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/" + self.var_out_file.get(
            )

        ##If there are no errors than run the string with Bowtie2
        ##Put the Output to the Screen from the program run
        ##If there are errors put them to the screen
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
                        text="OUTPUT: \n" + result.decode('utf-8'),
                        font="Times 18")
                else:
                    self.err_message.config(
                        text='\nERRORS: \n' + error.decode('utf-8'),
                        font="Times 18",
                        fg='dark red')
            else:
                self.err_message.config(
                    text="ERRORS: \n Makefile not in correct directory",
                    fg='dark red',
                    font="Times 18")
        else:
            self.err_message.config(
                text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")

        return

    ##Gives ability to Browse for a file and sets to a variable
    def browse_file_input1(self):
        self.var_filename = filedialog.askopenfilename()
        return

    def onFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return


if __name__ == "__main__":
    ##Start of App
    ##Creates Window and goes to the Mainloop of the class and creates the App
    root = Tk()
    root.wm_title("BOWTIE2 BUILD")
    root.geometry('900x300')
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
