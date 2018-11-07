import functions
import sys
import shlex
import subprocess
import os
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
## __init__ - Sets up the display of Sickle's main interface through
## buttons and labels
##
## MANDATORY - Sets up widgets for the mandatory options of App
##
## OPTIONAL - Sets up widgets for the optional options of App
##
## OPTIONS - Sets up display of options that one selects to be displayed
##
## Check_Options - Checks the widgets used and creates a string of options
## that get inputted to terminal to run Sickle
##
## browse_file_input1 - Lets user choose a file and puts the file path in a
## variable
##
## browse_file_input2 - Lets user choose a second file and puts the file path
## in a variable
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
            self.frame, text="Sickle", font="Times 24 bold", bg="white").grid(
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
            """Citation: Joshi NA, Fass JN. (2011). Sickle: A sliding-window, adaptive, quality-based trimming tool for FastQ files 
(Version 1.33) [Software].  Available at https://github.com/najoshi/sickle.""",
            font="Times 11 bold",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.fill_mandat = Label(
            self.frame,
            text="***Must fill all non-optional sections***",
            relief=FLAT,
            font="Times 20 bold",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_se_pe = StringVar()
        self.var_se_pe.set("Pick SE or PE       ")
        self.SE_PE = OptionMenu(
            self.frame,
            self.var_se_pe,
            "Single-end            ",
            "Paired-end",
            command=self.SE_and_PE)
        self.SE_PE.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="""Single-end or paired-end sequence trimming. Adjust input sequences before running program
such that they are of the same read length.""",
            relief=FLAT,
            justify=LEFT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_qual = StringVar()
        self.var_qual.set("Pick Quality Type")
        self.Qual = OptionMenu(self.frame, self.var_qual,
                               "Solexa/Illumina-1.0      ", "Illumina-1.5",
                               "Sanger/Illumina-1.8").grid(
                                   row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Type of quality values ",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_filename = ''
        self.browse_file1 = Button(
            self.frame,
            text="Browse",
            command=self.browse_file_input1,
            width=15)
        self.browse_file1.grid(row=x, column=0, padx=5, pady=5)
        self.label_filename = Label(
            self.frame,
            text=
            "Input File: Input filename with .fastq or .fq at end",
            relief=FLAT,
            bg="white")
        self.label_filename.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_reverse_file = ''
        self.browse_file2 = Button(
            self.frame,
            text="Browse",
            command=self.browse_file_input2,
            width=15)
        self.browse_file2.grid(row=x, column=0, padx=5, pady=(5, 60))
        self.label_reverse = Label(
            self.frame,
            text=
            "MANDATORY IF: you have separate files for forward and reverse reads, input reverse filename.",
            relief=FLAT,
            bg="white")
        self.label_reverse.grid(
            row=x, column=1, padx=5, pady=(5, 60), sticky="w")
        x += 1
        self.browse_file2.grid_remove()
        self.label_reverse.grid_remove()

        self.var_options = StringVar()
        self.var_options.set("Hide      			")
        self.options = OptionMenu(
            self.frame,
            self.var_options,
            "Display",
            "Hide",
            command=self.OPTIONS)
        self.options.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Display or Hide Extra Quality Filtering Options",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.run_button = Button(
            self.frame, text="Run Sickle", command=self.Check_Options)
        self.run_button.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.OPTIONAL(x)
        return

    def OPTIONAL(self, x):

        self.label_L = Label(
            self.frame,
            text="**OPTIONAL SECTION**",
            relief=FLAT,
            font="Times 20 bold",
            bg="white")
        self.label_L.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_out_file = StringVar()
        self.out_file = Entry(
            self.frame, textvariable=self.var_out_file, width=29)
        self.out_file.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_file.set('Output Filename')
        self.out_file_lab = Label(
            self.frame,
            text="Output File: Will default to TRIMMED_OUTPUT.fastq",
            relief=FLAT,
            bg="white")
        self.out_file_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_reverse_output = StringVar()
        self.reverse_out = Entry(
            self.frame, textvariable=self.var_reverse_output, width=29)
        self.reverse_out.grid(row=x, column=0, padx=5, pady=5)
        self.var_reverse_output.set('Trimmed PE Reverse Output Filename')
        self.label_reverse_out = Label(
            self.frame,
            text=
            "If you have separate files for forward and reverse reads, input reverse Output Filename. Must input singles file as well.",
            relief=FLAT,
            bg="white")
        self.label_reverse_out.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.reverse_out.grid_remove()
        self.label_reverse_out.grid_remove()

        self.var_singles = StringVar()
        self.singles_out = Entry(
            self.frame, textvariable=self.var_singles, width=29)
        self.singles_out.grid(row=x, column=0, padx=5, pady=5)
        self.var_singles.set('Trimmed Singles Filename')
        self.label_singles = Label(
            self.frame,
            text=
            "Trimmed Singles file output will default to TRIMMED_SINGLES.fastq",
            relief=FLAT,
            bg="white")
        self.label_singles.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.singles_out.grid_remove()
        self.label_singles.grid_remove()

        self.var_q_num = StringVar()
        self.q_num_entry = Entry(
            self.frame, textvariable=self.var_q_num, width=29)
        self.q_num_entry.grid(row=x, column=0, padx=5, pady=5)
        self.var_q_num.set('Quality Threshold: Input Integer')
        self.q_num_entry_lab = Label(
            self.frame,
            text=
            "Threshold for trimming based on average quality in a window. Default = 20.",
            relief=FLAT,
            bg="white")
        self.q_num_entry_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_L_num = StringVar()
        self.L_num_entry = Entry(
            self.frame, textvariable=self.var_L_num, width=29)
        self.L_num_entry.grid(row=x, column=0, padx=5, pady=5)
        self.var_L_num.set('Length Threshold: Input Integer')
        self.L_num_entry_lab = Label(
            self.frame,
            text=
            "Threshold to keep a read based on length after trimming. Default = 20.",
            relief=FLAT,
            bg="white")
        self.L_num_entry_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_n = IntVar()
        self.n_button = Checkbutton(
            self.frame, text="-n", variable=self.var_n, bg="white")
        self.n_button.grid(row=x, column=0, padx=5, pady=5)
        self.n_button_lab = Label(
            self.frame,
            text="Truncate sequences at position of first N.",
            relief=FLAT,
            bg="white")
        self.n_button_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_m = IntVar()
        self.m_button = Checkbutton(
            self.frame, text="-M", variable=self.var_m, bg="white")
        self.m_button.grid(row=x, column=0, padx=5, pady=5)
        self.label_m = Label(
            self.frame,
            text=
            "If you have one file with interleaved reads and you want ONLY one interleaved file as output. Cannot be used with singles file.",
            relief=FLAT,
            bg="white")
        self.label_m.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.m_button.grid_remove()
        self.label_m.grid_remove()

        self.var_x = IntVar()
        self.x_button = Checkbutton(
            self.frame, text="-x", variable=self.var_x, bg="white")
        self.x_button.grid(row=x, column=0, padx=5, pady=5)
        self.x_button_lab = Label(
            self.frame,
            text="Don't do five prime trimming.",
            relief=FLAT,
            bg="white")
        self.x_button_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_g = IntVar()
        self.g_button = Checkbutton(
            self.frame, text="-g", variable=self.var_g, bg="white")
        self.g_button.grid(row=x, column=0, padx=5, pady=5)
        self.g_button_lab = Label(
            self.frame,
            text="Output gzipped files.",
            relief=FLAT,
            bg="white")
        self.g_button_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.OPTIONS(x)

        self.err = StringVar()
        self.err_message = Message(
            self.frame, text=self.err.get(), aspect=1000, bg="white")
        self.err_message.grid(
            row=x, column=0, columnspan=5, padx=5, sticky="we")
        return

    def OPTIONS(self, x):

        self.out_file.grid_remove()
        self.reverse_out.grid_remove()
        self.label_reverse_out.grid_remove()
        self.singles_out.grid_remove()
        self.label_singles.grid_remove()
        self.q_num_entry.grid_remove()
        self.L_num_entry.grid_remove()
        self.n_button.grid_remove()
        self.m_button.grid_remove()
        self.label_m.grid_remove()
        self.x_button.grid_remove()
        self.g_button.grid_remove()
        self.out_file_lab.grid_remove()
        self.q_num_entry_lab.grid_remove()
        self.L_num_entry_lab.grid_remove()
        self.n_button_lab.grid_remove()
        self.x_button_lab.grid_remove()
        self.label_L.grid_remove(), self.g_button_lab.grid_remove()

        if (self.var_options.get() == "Display"):
            self.out_file.grid()
            self.reverse_out.grid()
            self.label_reverse_out.grid()
            self.singles_out.grid()
            self.label_singles.grid()
            self.q_num_entry.grid()
            self.L_num_entry.grid()
            self.n_button.grid()
            self.m_button.grid()
            self.label_m.grid()
            self.x_button.grid()
            self.g_button.grid()
            self.out_file_lab.grid()
            self.q_num_entry_lab.grid()
            self.L_num_entry_lab.grid()
            self.n_button_lab.grid()
            self.x_button_lab.grid()
            self.label_L.grid(), self.g_button_lab.grid()

        return

    def Check_Options(self):

        functions.globstring = "./GenCoF-master/Sickle/sickle-master/sickle"
        errors = ''

        if (self.var_se_pe.get() == "Paired-end"):
            functions.args_se_pe(self.var_se_pe.get())
            if (self.var_g.get()):
                functions.args_se_and_pe_non_man("-g", "")

            if (self.var_reverse_file == ''):

                if ((".fastq" not in self.var_filename
                     and ".fq" not in self.var_filename)
                        or self.var_filename == ''):
                    errors += "Enter file with .fastq or .fq appended to the end\n"
                else:
                    functions.file_input_inter(self.var_filename)

                if (self.var_qual.get() != "Pick Quality Type"):
                    functions.quality_vals(self.var_qual.get())
                else:
                    errors += "Enter quality type\n"

                if (self.var_m.get()):
                    if (self.var_g.get()):
                        if (self.var_out_file.get() == '' or
                                self.var_out_file.get() == 'Output Filename'):
                            functions.inter_big_m('TRIMMED_OUTPUT.fastq.gz')
                        elif (".fastq" not in self.var_out_file.get()
                              and ".fq" not in self.var_out_file.get()):
                            errors += "Enter file with .fastq or .fq appended to the end\n"
                        else:
                            functions.inter_big_m(
                                self.var_out_file.get() + '.gz')
                    else:
                        if (self.var_out_file.get() == '' or
                                self.var_out_file.get() == 'Output Filename'):
                            functions.inter_big_m('TRIMMED_OUTPUT.fastq')
                        elif (".fastq" not in self.var_out_file.get()
                              and ".fq" not in self.var_out_file.get()):
                            errors += "Enter file with .fastq or .fq appended to the end\n"
                        else:
                            functions.inter_big_m(self.var_out_file.get())

                else:
                    if (self.var_g.get()):
                        if (self.var_out_file.get() == '' or
                                self.var_out_file.get() == 'Output Filename'):
                            functions.inter_m('TRIMMED_OUTPUT.fastq.gz')
                        elif (".fastq" not in self.var_out_file.get()
                              and ".fq" not in self.var_out_file.get()):
                            errors += "Enter file with .fastq or .fq appended to the end\n"
                        else:
                            functions.inter_m(self.var_out_file.get() + '.gz')

                        if (self.var_singles.get() == ''
                                or self.var_singles.get() ==
                                'Trimmed Singles Filename'):
                            functions.trimmed('TRIMMED_SINGLES.fastq.gz')
                        elif (".fastq" not in self.var_singles.get()
                              and ".fq" not in self.var_singles.get()):
                            errors += "Enter file with .fastq or .fq appended to the end\n"
                        else:
                            functions.trimmed(self.var_singles.get() + '.gz')
                    else:
                        if (self.var_out_file.get() == '' or
                                self.var_out_file.get() == 'Output Filename'):
                            functions.inter_m('TRIMMED_OUTPUT.fastq')
                        elif (".fastq" not in self.var_out_file.get()
                              and ".fq" not in self.var_out_file.get()):
                            errors += "Enter file with .fastq or .fq appended to the end\n"
                        else:
                            functions.inter_m(self.var_out_file.get())

                        if (self.var_singles.get() == ''
                                or self.var_singles.get() ==
                                'Trimmed Singles Filename'):
                            functions.trimmed('TRIMMED_SINGLES.fastq')
                        elif (".fastq" not in self.var_singles.get()
                              and ".fq" not in self.var_singles.get()):
                            errors += "Enter file with .fastq or .fq appended to the end\n"
                        else:
                            functions.trimmed(self.var_singles.get())

            else:
                if ((".fastq" not in self.var_filename
                     and ".fq" not in self.var_filename)
                        or (self.var_filename == '')):
                    errors += "Enter file with .fastq or .fq appended to the end\n"
                else:
                    functions.file_input(self.var_filename)

                if (".fastq" not in self.var_reverse_file
                        and ".fq" not in self.var_reverse_file):
                    errors += "Enter file with .fastq or .fq appended to the end or clear contents of reverse entry\n"
                else:
                    functions.file_rev_input(self.var_reverse_file)

                if (self.var_qual.get() != "Pick Quality Type"):
                    functions.quality_vals(self.var_qual.get())
                else:
                    errors += "Enter quality value\n"

                if (self.var_g.get()):
                    if (self.var_out_file.get() == ''
                            or self.var_out_file.get() == 'Output Filename'):
                        functions.output('TRIMMED_OUTPUT.fastq.gz')
                    elif ('.fastq' not in self.var_out_file.get()
                          and ".fq" not in self.var_out_file.get()):
                        errors += "Enter file with .fastq or .fq appended to the end\n"
                    else:
                        functions.output(self.var_out_file.get() + '.gz')
                else:
                    if (self.var_out_file.get() == ''
                            or self.var_out_file.get() == 'Output Filename'):
                        functions.output('TRIMMED_OUTPUT.fastq')
                    elif ('.fastq' not in self.var_out_file.get()
                          and ".fq" not in self.var_out_file.get()):
                        errors += "Enter file with .fastq or .fq appended to the end\n"
                    else:
                        functions.output(self.var_out_file.get())

                if (self.var_g.get()):
                    if (self.var_reverse_output.get() == ''
                            or self.var_reverse_output.get() ==
                            'Trimmed PE Reverse Output Filename'):
                        functions.output_rev('TRIMMED_OUTPUT_REV.fastq.gz')
                    elif (".fastq" not in self.var_reverse_output.get()
                          and ".fq" not in self.var_reverse_output.get()):
                        errors += "Enter file with .fastq or .fq appended to the end\n"
                    else:
                        functions.output_rev(
                            self.var_reverse_output.get() + '.gz')
                else:
                    if (self.var_reverse_output.get() == ''
                            or self.var_reverse_output.get() ==
                            'Trimmed PE Reverse Output Filename'):
                        functions.output_rev('TRIMMED_OUTPUT_REV.fastq')
                    elif (".fastq" not in self.var_reverse_output.get()
                          and ".fq" not in self.var_reverse_output.get()):
                        errors += "Enter file with .fastq or .fq appended to the end\n"
                    else:
                        functions.output_rev(self.var_reverse_output.get())

                if (self.var_g.get()):
                    if (self.var_singles.get() == '' or self.var_singles.get()
                            == 'Trimmed Singles Filename'):
                        functions.trimmed('TRIMMED_SINGLES.fastq.gz')
                    elif (".fastq" not in self.var_singles.get()
                          and ".fq" not in self.var_singles.get()):
                        errors += "Enter file with .fastq or .fq appended to the end\n"
                    else:
                        functions.trimmed(self.var_singles.get() + '.gz')
                else:
                    if (self.var_singles.get() == '' or self.var_singles.get()
                            == 'Trimmed Singles Filename'):
                        functions.trimmed('TRIMMED_SINGLES.fastq')
                    elif (".fastq" not in self.var_singles.get()
                          and ".fq" not in self.var_singles.get()):
                        errors += "Enter file with .fastq or .fq appended to the end\n"
                    else:
                        functions.trimmed(self.var_singles.get())

        elif (self.var_se_pe.get() == "Single-end            "):
            functions.args_se_pe(self.var_se_pe.get())

            if ((".fastq" not in self.var_filename
                 and ".fq" not in self.var_filename)
                    or (self.var_filename == '')):
                errors += "Pick file with .fastq or .fq appended to the end\n"
            else:
                functions.file_input(self.var_filename)

            if (self.var_qual.get() != "Pick Quality Type"):
                functions.quality_vals(self.var_qual.get())
            else:
                errors += "Enter quality value\n"

            if (self.var_g.get()):
                if (self.var_out_file.get() == ''
                        or self.var_out_file.get() == 'Output Filename'):
                    functions.output('TRIMMED_OUTPUT.fastq.gz')
                elif (".fastq" not in self.var_out_file.get()
                      or ".fq" not in self.var_out_file.get()):
                    errors += "Enter file with .fastq or .fq appended to the end\n"
                else:
                    functions.output(self.var_out_file.get() + '.gz')

            else:
                if (self.var_out_file.get() == ''
                        or self.var_out_file.get() == 'Output Filename'):
                    functions.output('TRIMMED_OUTPUT.fastq')
                elif (".fastq" not in self.var_out_file.get()
                      or ".fq" not in self.var_out_file.get()):
                    errors += "Enter file with .fastq or .fq appended to the end\n"
                else:
                    functions.output(self.var_out_file.get())

        else:
            errors += "Enter SE or PE\n"

        if (functions.is_int(self.var_q_num.get())):
            functions.args_se_and_pe_non_man("-q", int(self.var_q_num.get()))

        if (functions.is_int(self.var_L_num.get())):
            functions.args_se_and_pe_non_man("-l", int(self.var_L_num.get()))

        if (self.var_x.get()):
            functions.args_se_and_pe_non_man("-x", "")

        if (self.var_n.get()):
            functions.args_se_and_pe_non_man("-n", "")

        self.err_message.config(text="Running....", font="Times 18")
        self.update()
        if (errors == ''):
            cmd_line = shlex.split(functions.globstring)
            if ('sickle' in os.listdir('./GenCoF-master/Sickle/sickle-master/')
                ):
                subprocess.call([
                    'chmod', '+x',
                    './GenCoF-master/Sickle/sickle-master/sickle'
                ])
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
                        font="Times 18")
            elif ('sickle' not in os.listdir(
                    './GenCoF-master/Sickle/sickle-master/') and 'Makefile' in
                  os.listdir('./GenCoF-master/Sickle/sickle-master/')):
                subprocess.call(
                    ["make", "-C", "./GenCoF-master/Sickle/sickle-master/"])
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
                    text="ERRORS: \n makefile not in correct directory",
                    fg='dark red',
                    font="Times 18")
        else:
            self.err_message.config(
                text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")

        return

    def SE_and_PE(self, another):

        if (self.var_se_pe.get() == "Paired-end"
                and self.var_options.get() == "Display"):
            self.browse_file2.grid()
            self.label_reverse.grid()
            self.reverse_out.grid()
            self.label_reverse_out.grid()
            self.label_filename.config(
                text=
                "MANDATORY: If you have one file with interleaved forward and reverse reads enter filename, otherwise enter paired-end forward fastq file"
            )
            self.singles_out.grid()
            self.label_singles.grid()
            self.m_button.grid()
            self.label_m.grid()

        if (self.var_se_pe.get() == "Paired-end"
                and self.var_options.get() != "Display"):
            self.browse_file2.grid()
            self.label_reverse.grid()
            self.label_filename.config(
                text=
                "MANDATORY: If you have one file with interleaved forward and reverse reads enter filename, otherwise enter paired-end forward fastq file"
            )

        elif (self.var_se_pe.get() == "Single-end            "):
            self.browse_file2.grid_remove()
            self.label_reverse.grid_remove()
            self.reverse_out.grid_remove()
            self.label_reverse_out.grid_remove()
            self.label_filename.config(
                text="MANDATORY: Input File: Input filename with .fastq at end"
            )
            self.singles_out.grid_remove()
            self.label_singles.grid_remove()
            self.m_button.grid_remove()
            self.label_m.grid_remove()

        return

    def browse_file_input1(self):
        self.var_filename = filedialog.askopenfilename()
        return

    def browse_file_input2(self):
        self.var_reverse_file = filedialog.askopenfilename()
        return

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return


if __name__ == "__main__":
    root = Tk()
    root.wm_title("SICKLE")
    root.geometry('975x575')
    App(root).pack(side="top", fill="both", expand=True)
    root.update_idletasks()
    root.mainloop()
