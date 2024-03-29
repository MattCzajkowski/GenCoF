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
# is_int - Checks if argument is an integer
# 
# Run - Closes window and opens GenCoF main
#
# App - Sets the window and grid of the app
#
## Functions within App:
## __init__ - Sets up the display of Bowtie2's main interface through
## buttons and labels
##
## MANDATORY - Sets up widgets for the mandatory options of App
##
## OPTIONAL - Sets up widgets for the optional options of App
##
## OPTIONAL_ALIGN - Sets up widgets for the alignment options of App
##
## SCORING - Sets up widgets for the scoring options of App
##
## PRESETS - Sets up widgets for the preset options of App
##
## EFFORT_PERFORMANCE_OPTIONS - Sets up widgets for the preset options of App
##
## PAIRED_OPTIONS - Sets up widgets for the paired-end options of App
##
## OPTIONS - Sets up display of options that one selects to be displayed
##
## Check_Options - Checks the widgets used and creates a string of options
## that get inputted to terminal to run Bowtie2
##
## SE_and_PE - Dynamically adds or subtracts widgets based on Single-end or
## paired-end being picked
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

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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
            self.frame, text="Bowtie2", font="Times 20 bold", bg="white").grid(
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
            text="***Must input file, sequence type and database(top 3 sections).  All other options can be left as default.***",
            relief=FLAT,
            font="Times 16 bold",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_se_pe = StringVar()
        self.var_se_pe.set("Pick SE, PE or Interleaved") 
        self.SE_PE = OptionMenu(
            self.frame,
            self.var_se_pe,
            "Single-end",
            "Paired-end",
            "Interleaved",
            command=self.SE_and_PE)
        self.SE_PE.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Single-end or paired-end sequence",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
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
            """Input File: Input filename with .fastq or .fasta at end that contains query sequences
If paired end files enter forward strand here.""",
            relief=FLAT,
            bg="white")
        self.label_filename.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_filename2 = ''
        self.browse_file2 = Button(
            self.frame,
            text="Browse",
            command=self.browse_file_input2,
            width=15)
        self.browse_file2.grid(row=x, column=0, padx=5, pady=5)
        self.label_filename2 = Label(
            self.frame,
            text=
            """Input File: Input filename with .fastq or .fasta at end that contains query sequences for paired end input
Enter reverse strand into this file input and forward strand into the first file input.""",
            relief=FLAT,
            bg="white")
        self.label_filename2.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.browse_file2.grid_remove()
        self.label_filename2.grid_remove()

        self.var_dbs = StringVar()
        self.dbs = Entry(
            self.frame, textvariable=self.var_dbs, width=28).grid(
                row=x, column=0, padx=5, pady=5)
        self.var_dbs.set('Input Database Name(s)')
        Label(
            self.frame,
            text=
            """Input Database Name(s): Names are according to their basenames in the folder bowtie2-2.3.4.
For example for the database files hg.1.bt2, hg.2.bt2 ... hg.rev.1.bt2, hg.rev.2.bt2 use "hg" as input. 
Make sure all database files are in the folder bowtie2-2.3.4.
For human genome use hg(version hs_ref_GRCh38_p7 from NCBI). Filters out
human DNA from samples and leaves what is leftover
(See http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml for adding databases.
Common databases can be downloaded easily through iGenomes.
See README.md for tutorial)""",
            relief=FLAT,
            justify=LEFT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_input = StringVar()
        self.var_input.set("Input File Type")
        self.input = OptionMenu(self.frame, self.var_input, "Fastq",
                                "Fasta or Multifasta", "QSEQ")
        self.input.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Query input files type. Defaults to fastq.",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_align_type = StringVar()
        self.var_align_type.set("Pick Alignment Type")
        self.align_type = OptionMenu(self.frame, self.var_align_type,
                                     "End to End", "Local")
        self.align_type.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text=
            """Type of alignment done. Local uses local alignment, ends might be soft clipped. 
Default is end to end which is entire read must align; no clipping.""",
            relief=FLAT,
            bg="white",
            justify=LEFT).grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_phred = StringVar()
        self.var_phred.set("Input Quality Type")
        self.phred = OptionMenu(self.frame, self.var_phred, "Phred 33",
                                "Phred 64")
        self.phred.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Quality values. Defaults to phred 33.",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.run_button = Button(
            self.frame, text="Run Bowtie2", command=self.Check_Options)
        self.run_button.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_options = StringVar()
        self.var_options.set("Display Options")
        self.options = OptionMenu(
            self.frame,
            self.var_options,
            "Quick Preset Options",
            "Output Options",
            "Alignment Options",
            "Scoring Options",
            "Effort and Performance Options",
            "Paired End Options",
            "Display No Options",
            command=self.OPTIONS)
        self.options.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Pick Options To Change Or Leave As Default",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.OPTIONAL(x)
        return

    def OPTIONAL(self, x):

        self.optional_lab = Label(
            self.frame,
            text="**Output Options**",
            relief=FLAT,
            font="Times 16 bold",
            bg="white")
        self.optional_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_out_unaligned = StringVar()
        self.out_unaligned = Entry(
            self.frame, textvariable=self.var_out_unaligned, width=28)
        self.out_unaligned.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_unaligned.set('Output Unaligned Filename')
        self.out_unaligned_lab = Label(
            self.frame,
            text=
            "Filename of reads that didn't align to index. Defaults to 'unaligned'.",
            relief=FLAT,
            bg="white")
        self.out_unaligned_lab.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_out_aligned = StringVar()
        self.out_aligned = Entry(
            self.frame, textvariable=self.var_out_aligned, width=28)
        self.out_aligned.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_aligned.set('Output Aligned Filename')
        self.out_aligned_lab = Label(
            self.frame,
            text=
            "Filename of reads that aligned to index. Defaults to 'aligned'.",
            relief=FLAT,
            bg="white")
        self.out_aligned_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_out_sam = StringVar()
        self.out_sam = Entry(
            self.frame, textvariable=self.var_out_sam, width=28)
        self.out_sam.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_sam.set('Output Sam Filename')
        self.out_sam_lab = Label(
            self.frame,
            text="File for SAM output. Defaults to 'SamFile'.",
            relief=FLAT,
            bg="white")
        self.out_sam_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.OPTIONAL_ALIGN(x)
        return

    def OPTIONAL_ALIGN(self, x):

        self.Optional_al_lab = Label(
            self.frame,
            text=
            "                                    **OPTIONAL: ALIGNMENT SECTION**                                  ",
            relief=FLAT,
            font="Times 16 bold",
            bg="white")
        self.Optional_al_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_N = StringVar()
        self.N = Entry(self.frame, textvariable=self.var_N, width=28)
        self.N.grid(row=x, column=0, padx=5, pady=5)
        self.var_N.set('Max Mismatches: Input 0 or 1')
        self.N_lab = Label(
            self.frame,
            text=
            """Max integer mismatches in seed alignment; can be 0 or 1. Default is 0.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.N_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_length = StringVar()
        self.length = Entry(self.frame, textvariable=self.var_length, width=28)
        self.length.grid(row=x, column=0, padx=5, pady=5)
        self.var_length.set('Length of Seed: Input Integer')
        self.length_lab = Label(
            self.frame,
            text=
            """Length of seed substrings; must be >3 and <32. Default is 22.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.length_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_i = StringVar()
        self.i = Entry(self.frame, textvariable=self.var_i, width=28)
        self.i.grid(row=x, column=0, padx=5, pady=5)
        self.var_i.set('Seed Interval: Input Function')
        self.i_lab = Label(
            self.frame,
            text=
            "Interval between seed substrings w/r/t read length. Default is S,1,1.15.",
            relief=FLAT,
            bg="white")
        self.i_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_n_ceil = StringVar()
        self.n_ceil = Entry(self.frame, textvariable=self.var_n_ceil, width=28)
        self.n_ceil.grid(row=x, column=0, padx=5, pady=5)
        self.var_n_ceil.set('N Ceiling: Input Function')
        self.n_ceil_lab = Label(
            self.frame,
            text=
            "Func for max integer of non_A/C/G/Ts permitted in aln. Default is L,0,0.15.",
            relief=FLAT,
            bg="white")
        self.n_ceil_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_dpad = StringVar()
        self.dpad = Entry(self.frame, textvariable=self.var_dpad, width=28)
        self.dpad.grid(row=x, column=0, padx=5, pady=5)
        self.var_dpad.set('Ref Chars: Input Integer')
        self.dpad_lab = Label(
            self.frame,
            text=
            "Include integer of extra ref chars on sides of DP table. Default is 15.",
            relief=FLAT,
            bg="white")
        self.dpad_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_gbar = StringVar()
        self.gbar = Entry(self.frame, textvariable=self.var_gbar, width=28)
        self.gbar.grid(row=x, column=0, padx=5, pady=5)
        self.var_gbar.set('Disallow Gaps: Input Integer')
        self.gbar_lab = Label(
            self.frame,
            text=
            "Disallow gaps within integer of nucs of read extremes. Default is 4.",
            relief=FLAT,
            bg="white")
        self.gbar_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_ignore_quals = IntVar()
        self.ignore_quals_button = Checkbutton(
            self.frame,
            text="Ignore Quals",
            variable=self.var_ignore_quals,
            bg="white")
        self.ignore_quals_button.grid(row=x, column=0, padx=5, pady=5)
        self.ignore_quals_lab = Label(
            self.frame,
            text="Treat all quality values as 30 on Phred scale.",
            relief=FLAT,
            bg="white")
        self.ignore_quals_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_nofw = IntVar()
        self.nofw_button = Checkbutton(
            self.frame, text="No Forward", variable=self.var_nofw, bg="white")
        self.nofw_button.grid(row=x, column=0, padx=5, pady=5)
        self.nofw_lab = Label(
            self.frame,
            text="Do not align forward (original) version of read.",
            relief=FLAT,
            bg="white")
        self.nofw_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_norc = IntVar()
        self.norc_button = Checkbutton(
            self.frame, text="No Reverse", variable=self.var_norc, bg="white")
        self.norc_button.grid(row=x, column=0, padx=5, pady=5)
        self.norc_lab = Label(
            self.frame,
            text="Do not align reverse complement version of read.",
            relief=FLAT,
            bg="white")
        self.norc_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_no_mm_upfront = IntVar()
        self.no_mm_upfront_button = Checkbutton(
            self.frame,
            text="No Mismatch",
            variable=self.var_no_mm_upfront,
            bg="white")
        self.no_mm_upfront_button.grid(row=x, column=0, padx=5, pady=5)
        self.no_mm_upfront_lab = Label(
            self.frame,
            text=
            "Do not allow 1 mismatch alignments before attempting to scan for the optimal seeded alignments.",
            relief=FLAT,
            bg="white")
        self.no_mm_upfront_lab.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_qc_filter = IntVar()
        self.qc_filter_button = Checkbutton(
            self.frame,
            text="QC Filter",
            variable=self.var_qc_filter,
            bg="white")
        self.qc_filter_button.grid(row=x, column=0, padx=5, pady=5)
        self.qc_filter_lab = Label(
            self.frame,
            text=
            "Filter out reads that are bad according to QSEQ filter.",
            relief=FLAT,
            bg="white")
        self.qc_filter_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.SCORING(x)

    def SCORING(self, x):

        self.scoring_lab = Label(
            self.frame,
            text="**Scoring Options**",
            relief=FLAT,
            font="Times 16 bold",
            bg="white")
        self.scoring_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_ma = StringVar()
        self.ma = Entry(self.frame, textvariable=self.var_ma, width=28)
        self.ma.grid(row=x, column=0, padx=5, pady=5)
        self.var_ma.set('Match Bonus: Input Integer')
        self.ma_lab = Label(
            self.frame,
            text=
            "Match bonus. Default is 0 for end to end, 2 for local",
            relief=FLAT,
            bg="white")
        self.ma_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_mp = StringVar()
        self.mp = Entry(self.frame, textvariable=self.var_mp, width=28)
        self.mp.grid(row=x, column=0, padx=5, pady=5)
        self.var_mp.set('Max Penalty: Input Integer')
        self.mp_lab = Label(
            self.frame,
            text=
            "Max penalty for mismatch; lower qual = lower penalty. Default is 6.",
            relief=FLAT,
            bg="white")
        self.mp_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_np = StringVar()
        self.np = Entry(self.frame, textvariable=self.var_np, width=28)
        self.np.grid(row=x, column=0, padx=5, pady=5)
        self.var_np.set('Non ACGT Penalty: Input Integer')
        self.np_lab = Label(
            self.frame,
            text=
            "Penalty for non-A/C/G/Ts in read/ref. Default is 1.",
            relief=FLAT,
            bg="white")
        self.np_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_rdg = StringVar()
        self.rdg = Entry(self.frame, textvariable=self.var_rdg, width=28)
        self.rdg.grid(row=x, column=0, padx=5, pady=5)
        self.var_rdg.set('Penalties: Input Integers')
        self.rdg_lab = Label(
            self.frame,
            text=
            "Read gap open and extend penalties respectively. Default is 5,3.",
            relief=FLAT,
            bg="white")
        self.rdg_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_rfg = StringVar()
        self.rfg = Entry(self.frame, textvariable=self.var_rfg, width=28)
        self.rfg.grid(row=x, column=0, padx=5, pady=5)
        self.var_rfg.set('Penalties: Input Integers')
        self.rfg_lab = Label(
            self.frame,
            text=
            "Reference gap open and extend penalties respectively. Default is 5,3.",
            relief=FLAT,
            bg="white")
        self.rfg_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_score_min = StringVar()
        self.score_min = Entry(
            self.frame, textvariable=self.var_score_min, width=28)
        self.score_min.grid(row=x, column=0, padx=5, pady=5)
        self.var_score_min.set('Min Alignment: Input String')
        self.score_min_lab = Label(
            self.frame,
            text="""Min acceptable alignment score w/r/t read length 
Default is G,20,8 for local, L,-0.6,-0.6 for end-to-end""",
            relief=FLAT,
            bg="white",
            justify=LEFT)
        self.score_min_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.PRESETS(x)

    def PRESETS(self, x):

        self.presets_lab = Label(
            self.frame,
            text="**Quick Optimality Options**",
            relief=FLAT,
            font="Times 16 bold",
            bg="white")
        self.presets_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.presets_info_lab = Label(
            self.frame,
            text="""Where -D is give up extending after number of failed extends
-R is for reads with repetitive seeds, try number sets of seeds
-N is max number of mismatches
-L is length of seed substrings
-i is interval between seed substrings w/r/t read len""",
            relief=FLAT,
            bg="white",
            justify=LEFT)
        self.presets_info_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5)
        x += 1

        self.var_end_to_end = StringVar()
        self.var_end_to_end.set("Quick Preset Alignments")
        self.end_to_end = OptionMenu(self.frame, self.var_end_to_end,
                                     "Very Fast", "Fast", "Sensitive",
                                     "Very Sensitive")
        self.end_to_end.grid(row=x, column=0, padx=5, pady=5)
        self.end_to_end_lab = Label(
            self.frame,
            text="""                  FOR END TO END
very-fast        -D 5 -R 1 -N 0 -L 22 -i S,0,2.50
fast                -D 10 -R 2 -N 0 -L 22 -i S,0,2.50
sensitive         -D 15 -R 2 -N 0 -L 22 -i S,1,1.15 (default)
very-sensitive -D 20 -R 3 -N 0 -L 20 -i S,1,0.50""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.end_to_end_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_local = StringVar()
        self.var_local.set("Quick Preset Alignments")
        self.local = OptionMenu(self.frame, self.var_local, "Very Fast Local",
                                "Fast Local", "Sensitive Local",
                                "Very Sensitive Local")
        self.local.grid(row=x, column=0, padx=5, pady=5)
        self.local_lab = Label(
            self.frame,
            text="""                  FOR LOCAL
very-fast-local         -D 5 -R 1 -N 0 -L 25 -i S,1,2.00
fast-local                 -D 10 -R 2 -N 0 -L 22 -i S,1,1.75
sensitive-local         -D 15 -R 2 -N 0 -L 20 -i S,1,0.75 (default)
very-sensitive-local -D 20 -R 3 -N 0 -L 20 -i S,1,0.50""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.local_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.EFFORT_PERFORMANCE_OPTIONS(x)

    def EFFORT_PERFORMANCE_OPTIONS(self, x):

        self.effort_perform_lab = Label(
            self.frame,
            text="**Effort and Performance Options**",
            relief=FLAT,
            font="Times 16 bold",
            bg="white")
        self.effort_perform_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_D = StringVar()
        self.D = Entry(self.frame, textvariable=self.var_D, width=28)
        self.D.grid(row=x, column=0, padx=5, pady=5)
        self.var_D.set('Extension Failed: Input Integer')
        self.D_lab = Label(
            self.frame,
            text=
            "Give up extending after integer of failed extends in a row. Default is 15.",
            relief=FLAT,
            bg="white")
        self.D_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_R = StringVar()
        self.R = Entry(self.frame, textvariable=self.var_R, width=28)
        self.R.grid(row=x, column=0, padx=5, pady=5)
        self.var_R.set('Sets of Seeds: Input Integer')
        self.R_lab = Label(
            self.frame,
            text=
            "For reads w/ repetitive seeds, try integer sets of seeds. Default is 2.",
            relief=FLAT,
            bg="white")
        self.R_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_threads = StringVar()
        self.threads = Entry(
            self.frame, textvariable=self.var_threads, width=28)
        self.threads.grid(row=x, column=0, padx=5, pady=5)
        self.var_threads.set('Threads: Input Integer')
        self.threads_lab = Label(
            self.frame,
            text=
            "Number of alignment threads to launch. Default is 1.",
            relief=FLAT,
            bg="white")
        self.threads_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_mm = IntVar()
        self.mm_button = Checkbutton(
            self.frame, text="Memory Mapped", variable=self.var_mm, bg="white")
        self.mm_button.grid(row=x, column=0, padx=5, pady=5)
        self.mm_lab = Label(
            self.frame,
            text=
            "Use memory-mapped I/O for index; many 'bowtie's can share.",
            relief=FLAT,
            bg="white")
        self.mm_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.PAIRED_OPTIONS(x)

    def PAIRED_OPTIONS(self, x):

        self.paired_lab = Label(
            self.frame,
            text="**Paired End Options**",
            relief=FLAT,
            font="Times 16 bold",
            bg="white")
        self.paired_lab.grid(
            row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        self.var_minins = StringVar()
        self.minins = Entry(self.frame, textvariable=self.var_minins, width=28)
        self.minins.grid(row=x, column=0, padx=5, pady=5)
        self.var_minins.set('Fragment Length: Input Integer')
        self.minins_lab = Label(
            self.frame,
            text="Minimum fragment length. Default is 0.",
            relief=FLAT,
            bg="white")
        self.minins_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_maxins = StringVar()
        self.maxins = Entry(self.frame, textvariable=self.var_maxins, width=28)
        self.maxins.grid(row=x, column=0, padx=5, pady=5)
        self.var_maxins.set('Fragment Length: Input Integer')
        self.maxins_lab = Label(
            self.frame,
            text="Maximum fragment length. Default is 500.",
            relief=FLAT,
            bg="white")
        self.maxins_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_no_mixed = IntVar()
        self.no_mixed_button = Checkbutton(
            self.frame,
            text="Suppress Unpaired",
            variable=self.var_no_mixed,
            bg="white")
        self.no_mixed_button.grid(row=x, column=0, padx=5, pady=5)
        self.no_mixed_lab = Label(
            self.frame,
            text="Suppress unpaired alignments for paired reads.",
            relief=FLAT,
            bg="white")
        self.no_mixed_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_no_discordant = IntVar()
        self.no_discordant_button = Checkbutton(
            self.frame,
            text="Suppress Discordant",
            variable=self.var_no_discordant,
            bg="white")
        self.no_discordant_button.grid(row=x, column=0, padx=5, pady=5)
        self.no_discordant_lab = Label(
            self.frame,
            text="Suppress discordant alignments for paired reads.",
            relief=FLAT,
            bg="white")
        self.no_discordant_lab.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_dovetail = IntVar()
        self.dovetail_button = Checkbutton(
            self.frame,
            text="Concordant",
            variable=self.var_dovetail,
            bg="white")
        self.dovetail_button.grid(row=x, column=0, padx=5, pady=5)
        self.dovetail_lab = Label(
            self.frame,
            text="Concordant when mates extend past each other.",
            relief=FLAT,
            bg="white")
        self.dovetail_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_no_contain = IntVar()
        self.no_contain_button = Checkbutton(
            self.frame,
            text="No Contain",
            variable=self.var_no_contain,
            bg="white")
        self.no_contain_button.grid(row=x, column=0, padx=5, pady=5)
        self.no_contain_lab = Label(
            self.frame,
            text=
            "Not concordant when one mate alignment contains other.",
            relief=FLAT,
            bg="white")
        self.no_contain_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.var_no_overlap = IntVar()
        self.no_overlap_button = Checkbutton(
            self.frame,
            text="No Overlap",
            variable=self.var_no_overlap,
            bg="white")
        self.no_overlap_button.grid(row=x, column=0, padx=5, pady=5)
        self.no_overlap_lab = Label(
            self.frame,
            text="Not concordant when mates overlap at all.",
            relief=FLAT,
            bg="white")
        self.no_overlap_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        self.OPTIONS(x)

        self.err = StringVar()
        self.err_message = Message(
            self.frame, text=self.err.get(), aspect=1000, bg="white")
        self.err_message.grid(
            row=x, column=0, columnspan=5, padx=5, sticky="w")

        return

    def OPTIONS(self, x):

        self.optional_lab.grid_remove()
        self.out_unaligned.grid_remove()
        self.out_unaligned_lab.grid_remove()
        self.out_aligned.grid_remove()
        self.out_aligned_lab.grid_remove()
        self.out_sam.grid_remove()
        self.out_sam_lab.grid_remove()
        self.Optional_al_lab.grid_remove()
        self.N.grid_remove()
        self.N_lab.grid_remove()
        self.length.grid_remove()
        self.length_lab.grid_remove()
        self.i.grid_remove()
        self.i_lab.grid_remove()
        self.n_ceil.grid_remove()
        self.n_ceil_lab.grid_remove()
        self.dpad.grid_remove()
        self.dpad_lab.grid_remove()
        self.gbar.grid_remove()
        self.gbar_lab.grid_remove()
        self.ignore_quals_button.grid_remove()
        self.ignore_quals_lab.grid_remove()
        self.nofw_button.grid_remove()
        self.nofw_lab.grid_remove()
        self.norc_button.grid_remove()
        self.norc_lab.grid_remove()
        self.no_mm_upfront_button.grid_remove()
        self.no_mm_upfront_lab.grid_remove()
        self.qc_filter_button.grid_remove()
        self.qc_filter_lab.grid_remove()
        self.scoring_lab.grid_remove()
        self.ma.grid_remove()
        self.ma_lab.grid_remove()
        self.mp.grid_remove()
        self.mp_lab.grid_remove()
        self.np.grid_remove()
        self.np_lab.grid_remove()
        self.rdg.grid_remove()
        self.rdg_lab.grid_remove()
        self.rfg.grid_remove()
        self.rfg_lab.grid_remove()
        self.score_min.grid_remove()
        self.score_min_lab.grid_remove()
        self.presets_lab.grid_remove()
        self.end_to_end.grid_remove()
        self.end_to_end_lab.grid_remove()
        self.local.grid_remove()
        self.local_lab.grid_remove()
        self.effort_perform_lab.grid_remove()
        self.D.grid_remove()
        self.D_lab.grid_remove()
        self.R.grid_remove()
        self.R_lab.grid_remove()
        self.threads.grid_remove()
        self.threads_lab.grid_remove()
        self.mm_button.grid_remove()
        self.mm_lab.grid_remove()
        self.paired_lab.grid_remove()
        self.minins.grid_remove()
        self.minins_lab.grid_remove()
        self.maxins.grid_remove()
        self.maxins_lab.grid_remove()
        self.no_mixed_button.grid_remove()
        self.no_mixed_lab.grid_remove()
        self.no_discordant_button.grid_remove()
        self.no_discordant_lab.grid_remove()
        self.dovetail_button.grid_remove()
        self.dovetail_lab.grid_remove()
        self.no_contain_button.grid_remove()
        self.no_contain_lab.grid_remove()
        self.no_overlap_button.grid_remove()
        self.no_overlap_lab.grid_remove()
        self.presets_info_lab.grid_remove()

        if (self.var_options.get() == "Quick Preset Options"):
            self.presets_lab.grid()
            self.end_to_end.grid()
            self.end_to_end_lab.grid()
            self.local.grid()
            self.local_lab.grid()
            self.presets_info_lab.grid()
        elif (self.var_options.get() == "Output Options"):
            self.optional_lab.grid()
            self.out_unaligned.grid()
            self.out_unaligned_lab.grid()
            self.out_aligned.grid()
            self.out_aligned_lab.grid()
            self.out_sam.grid()
            self.out_sam_lab.grid()
        elif (self.var_options.get() == "Alignment Options"):
            self.Optional_al_lab.grid()
            self.N.grid()
            self.N_lab.grid()
            self.length.grid()
            self.length_lab.grid()
            self.i.grid()
            self.i_lab.grid()
            self.n_ceil.grid()
            self.n_ceil_lab.grid()
            self.dpad.grid()
            self.dpad_lab.grid()
            self.gbar.grid()
            self.gbar_lab.grid()
            self.ignore_quals_button.grid()
            self.ignore_quals_lab.grid()
            self.nofw_button.grid()
            self.nofw_lab.grid()
            self.norc_button.grid()
            self.norc_lab.grid()
            self.no_mm_upfront_button.grid()
            self.no_mm_upfront_lab.grid()
            self.qc_filter_button.grid()
            self.qc_filter_lab.grid()
        elif (self.var_options.get() == "Scoring Options"):
            self.scoring_lab.grid()
            self.ma.grid()
            self.ma_lab.grid()
            self.mp.grid()
            self.mp_lab.grid()
            self.np.grid()
            self.np_lab.grid()
            self.rdg.grid()
            self.rdg_lab.grid()
            self.rfg.grid()
            self.rfg_lab.grid()
            self.score_min.grid()
            self.score_min_lab.grid()
        elif (self.var_options.get() == "Effort and Performance Options"):
            self.effort_perform_lab.grid()
            self.D.grid()
            self.D_lab.grid()
            self.R.grid()
            self.R_lab.grid()
            self.threads.grid()
            self.threads_lab.grid()
            self.mm_button.grid()
            self.mm_lab.grid()
        elif (self.var_options.get() == "Paired End Options"):
            self.paired_lab.grid()
            self.minins.grid()
            self.minins_lab.grid()
            self.maxins.grid()
            self.maxins_lab.grid()
            self.no_mixed_button.grid()
            self.no_mixed_lab.grid()
            self.no_discordant_button.grid()
            self.no_discordant_lab.grid()
            self.dovetail_button.grid()
            self.dovetail_lab.grid()
            self.no_contain_button.grid()
            self.no_contain_lab.grid()
            self.no_overlap_button.grid()
            self.no_overlap_lab.grid()
        return

    def Check_Options(self):

        globstring = "./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/bowtie2 "
        errors = ''

        if (self.var_input.get() == "Fasta or Multifasta"):
            globstring += "-f "
        if (self.var_input.get() == "QSEQ"):
            globstring += "--qseq "
        if (self.var_align_type.get() == "Local"):
            globstring += "--local "
        if (self.var_phred.get() == "Phred 64"):
            globstring += "--phred64 "

        if (self.var_se_pe.get() == "Paired-end"
                or self.var_se_pe.get() == "Interleaved"):
            if (self.var_out_unaligned.get() != "Output Unaligned Filename"
                    and self.var_out_unaligned.get() != ""):
                globstring += "--un-conc " + self.var_out_unaligned.get() + " "
            else:
                globstring += "--un-conc unaligned "

            if (self.var_out_aligned.get() != "Output Aligned Filename"
                    and self.var_out_aligned.get() != ""):
                globstring += "--al-conc " + self.var_out_aligned.get() + " "
            else:
                globstring += "--al-conc aligned "

        if (self.var_se_pe.get() == "Single-end"):
            if (self.var_out_unaligned.get() != "Output Unaligned Filename"
                    and self.var_out_unaligned.get() != ""):
                globstring += "--un " + self.var_out_unaligned.get() + " "
            else:
                globstring += "--un unaligned "

            if (self.var_out_aligned.get() != "Output Aligned Filename"
                    and self.var_out_aligned.get() != ""):
                globstring += "--al " + self.var_out_aligned.get() + " "
            else:
                globstring += "--al aligned "

        if (is_int(self.var_N.get())):
            globstring += "-N " + self.var_N.get() + " "
        if (is_int(self.var_length.get())):
            globstring += "-L " + self.var_length.get() + " "
        if (self.var_i.get() != "Seed Interval: Input Function"
                and self.var_i.get() != ""):
            globstring += "-i " + self.var_i.get() + " "
        if (self.var_n_ceil.get() != "N Ceiling: Input Function"
                and self.var_n_ceil.get() != ""):
            globstring += "--n-ceil " + self.var_n_ceil.get() + " "
        if (is_int(self.var_dpad.get())):
            globstring += "--dpad " + self.var_dpad.get() + " "
        if (is_int(self.var_gbar.get())):
            globstring += "--gbar " + self.var_gbar.get() + " "
        if (self.var_ignore_quals.get()):
            globstring += "--ignore-quals "
        if (self.var_nofw.get()):
            globstring += "--nofw "
        if (self.var_norc.get()):
            globstring += "--norc "
        if (self.var_no_mm_upfront.get()):
            globstring += "--no-1mm-upfront "
        if (self.var_qc_filter.get()):
            globstring += "--qc-filter "
        if (is_int(self.var_ma.get())):
            globstring += "--ma " + self.var_ma.get() + " "
        if (is_int(self.var_mp.get())):
            globstring += "--mp " + self.var_mp.get() + " "
        if (is_int(self.var_np.get())):
            globstring += "--np " + self.var_np.get() + " "
        if (self.var_rdg.get() != "Penalties: Input Integers"
                and self.var_rdg.get() != ""):
            globstring += "--rdg " + self.var_rdg.get() + " "
        if (self.var_rfg.get() != "Penalties: Input Integers"
                and self.var_rfg.get() != ""):
            globstring += "--rfg " + self.var_rfg.get() + " "
        if (self.var_score_min.get() != "Min Alignment: Input String"
                and self.var_score_min.get() != ""):
            globstring += "--score-min " + self.var_score_min.get() + " "

        if (self.var_end_to_end.get() == "Very Fast"):
            globstring += "--very-fast "
        if (self.var_end_to_end.get() == "Fast"):
            globstring += "--fast "
        if (self.var_end_to_end.get() == "Very Sensitive"):
            globstring += "--very-sensitive "

        if (self.var_local.get() == "Very Fast Local"):
            globstring += "--very-fast-local "
        if (self.var_local.get() == "Fast Local"):
            globstring += "--fast-local "
        if (self.var_local.get() == "Very Sensitive Local"):
            globstring += "--very-sensitive-local "

        if (is_int(self.var_D.get())):
            globstring += "-D " + self.var_D.get() + " "
        if (is_int(self.var_R.get())):
            globstring += "-R " + self.var_R.get() + " "
        if (is_int(self.var_threads.get())):
            globstring += "--threads " + self.var_threads.get() + " "
        if (self.var_mm.get()):
            globstring += "--mm "

        if (is_int(self.var_minins.get())):
            globstring += "--minins " + self.var_minins.get() + " "
        if (is_int(self.var_maxins.get())):
            globstring += "--maxins " + self.var_maxins.get() + " "
        if (self.var_no_mixed.get()):
            globstring += "--no-mixed "
        if (self.var_no_discordant.get()):
            globstring += "--no-discordant "
        if (self.var_dovetail.get()):
            globstring += "--dovetail "
        if (self.var_no_contain.get()):
            globstring += "--no-contain "
        if (self.var_no_overlap.get()):
            globstring += "--no-overlap "

        if (self.var_dbs.get() != "Input Database Name(s)"
                and self.var_dbs.get() != ""):
            globstring += "-x ./GenCoF-master/Bowtie2/bowtie2-2.3.4.1/" + self.var_dbs.get(
            ) + " "
        else:
            errors += "Enter Database Basename\n"

        if (self.var_se_pe.get() == "Single-end"):
            if (self.var_filename != ""):
                globstring += "-U " + "'" + self.var_filename + "'" + " "
            else:
                errors += "Enter Input File\n"
        elif (self.var_se_pe.get() == "Paired-end"):
            if (self.var_filename != "" and self.var_filename2 != ""):
                globstring += "-1 " + "'" + self.var_filename + "'" + " -2 " + "'" + self.var_filename2 + "'" + " "
            else:
                errors += "Enter Input Files\n"
        elif (self.var_se_pe.get() == "Interleaved"):
            if (self.var_filename != ""):
                globstring += "--interleaved " + "'" + self.var_filename + "'" + " "
            else:
                errors += "Enter Input Files\n"
        else:
            errors += "Enter Input File Type\n"
        if (self.var_out_sam.get() != "Output Sam Filename"
                and self.var_out_sam.get() != ""):
            globstring += "-S " + self.var_out_sam.get() + " "
        else:
            globstring += "-S SamFile "

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
                    fg='dark red',
                    font="Times 18")
        else:
            self.err_message.config(
                text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")

        return

    def SE_and_PE(self, another): 
        if (self.var_se_pe.get() == "Paired-end"):
            self.browse_file2.grid()
            self.label_filename2.grid()

        elif (self.var_se_pe.get() == "Single-end"
              or self.var_se_pe.get() == "Interleaved"):
            self.browse_file2.grid_remove()
            self.label_filename2.grid_remove()

        return

    def browse_file_input1(self):
        self.var_filename = filedialog.askopenfilename()
        return

    def browse_file_input2(self):
        self.var_filename2 = filedialog.askopenfilename()
        return

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return


if __name__ == "__main__":
    root = Tk()
    root.wm_title("BOWTIE2")
    root.geometry('1050x610')
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
