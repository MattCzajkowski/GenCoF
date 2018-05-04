import functions, shlex, subprocess, sys, os
from tkinter import filedialog
from tkinter import *

#Requires Perl modules (all modules included with perl download) Data::Dumper, Getopt::Long, Pod::Usage, File::Path >= 2.07, Cwd,
## FindBin and Python3 Tkinter


##Closes window and opens window run
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
        ##Start to Create the grid build of GUI##

        ##Sets up the frame of the window as well as adding a scrollbar
        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0, bg="white")
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

        ##Title of Prinseq Portion of GUI##
        self.file1_title = Label(
            self.frame, text="Prinseq", font="Times 24 bold", bg="white").grid(
                row=x,
                column=0,
                columnspan=10,
                padx=5,
                pady=(5, 5),
                sticky="we")
        x += 1

        ##Citation for Prinseq
        self.fill_mandat = Label(
            self.frame,
            text=
            "Citation: Schmieder R and Edwards R: Quality control and preprocessing of metagenomic datasets. Bioinformatics 2011, 27:863-864.",
            font="Times 11 bold",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        ##Title for Mandatory Section
        self.fill_mandat = Label(
            self.frame,
            text="***Must fill all MANDATORY sections***",
            relief=FLAT,
            font="Times 20 bold",
            bg="white").grid(
                row=x, column=0, columnspan=10, padx=5, pady=5, sticky="we")
        x += 1

        ##Input File Type Section
        self.var_file_type = StringVar()
        self.var_file_type.set("Pick Input File Type")  # default
        self.file_type = OptionMenu(
            self.frame,
            self.var_file_type,
            "Fastq File",
            "Fasta File",
            "Amino Acid File",
            "Paired-end Fastq File",
            "Paired-end Fasta File",
            command=self.FILE_TYPE)
        self.file_type.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="MANDATORY: single-end or paired-end sequence trimming",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Filename Section
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
            "MANDATORY: Input File. Avoid spaces with folder names as this can cause errors.",
            relief=FLAT,
            bg="white")
        self.label_filename.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.browse_file1.grid_remove()
        self.label_filename.grid_remove()

        ##Input Paired-End File Section
        self.var_paired_file = ''
        self.browse_file2 = Button(
            self.frame,
            text="Browse",
            command=self.browse_file_input2,
            width=15)
        self.browse_file2.grid(row=x, column=0, padx=5, pady=5)
        self.label_filename2 = Label(
            self.frame,
            text=
            """MANDATORY: Input Reverse Strand File. The sequence identifiers for two matching
paired-end sequences in separate files can be marked by
/1 and /2, or _L and _R, or _left and _right,
or must have the exact same identifier in both input files. 
The input sequences must be sorted by their sequence identifiers. 
Singletons are allowed in the input files.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.label_filename2.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.browse_file2.grid_remove()
        self.label_filename2.grid_remove()

        #Input Phred Format Section
        self.var_phred = IntVar()
        self.phred_button = Checkbutton(
            self.frame, text="phred64", variable=self.var_phred)
        self.phred_button.grid(row=x, column=0, padx=5, pady=5)
        self.phred_lab = Label(
            self.frame,
            text="MANDATORY: Quality data in FASTQ file is in Phred+64 format ",
            relief=FLAT,
            bg="white")
        self.phred_lab.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.phred_button.grid_remove()
        self.phred_lab.grid_remove()

        #Pick Options to Change Section
        self.var_options = StringVar()
        self.var_options.set("Pick Options To Change")  # default
        self.options = OptionMenu(
            self.frame,
            self.var_options,
            "Output Options",
            "Filter Options",
            "Trim Options",
            "Reformat Options",
            "Summary Statistic Options",
            command=self.OPTIONS)
        self.options.grid(row=x, column=0, padx=5, pady=5)
        Label(
            self.frame,
            text="Pick Options To Change Or Leave As Default",
            relief=FLAT,
            bg="white").grid(
                row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Run Button which goes to function: Check_Options when clicked
        self.run_button = Button(
            self.frame, text="Run Prinseq", command=self.Check_Options)
        self.run_button.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1
        self.run_button.grid_remove()

        ##Error Output To Screen Label
        self.err = StringVar()
        self.err_message = Message(
            self.frame, text=self.err.get(), aspect=1000, bg="white")
        self.err_message.grid(
            row=x, column=0, columnspan=5, padx=5, sticky="we")

        ##Go To Build Output Section
        self.OUTPUT(x)

        return

    def OUTPUT(self, x):

        ##Title of Output Portion of GUI##
        self.output_title = Label(
            self.frame, text="Output Options", relief=RAISED, bg="white")
        self.output_title.grid(
            row=x, column=0, columnspan=10, padx=5, pady=(5, 30), sticky="we")
        x += 1

        ##Input Output Format Section
        self.out_format = StringVar()
        self.out_format.set("Output Format")  # default
        self.o_format = OptionMenu(self.frame, self.out_format, "FASTA only",
                                   "FASTA and QUAL", "FASTQ",
                                   "FASTQ and FASTA", "FASTQ, FASTA and QUAL",
                                   "Leave As Default")
        self.o_format.grid(row=x, column=0, padx=5, pady=5)
        self.o_format_label = Label(
            self.frame,
            text="Output Format. Default to same as input.",
            relief=FLAT,
            bg="white")
        self.o_format_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Out Good Section
        self.var_out_good = StringVar()
        self.out_good = Entry(
            self.frame, textvariable=self.var_out_good, width=28)
        self.out_good.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_good.set('Output filename for Good')
        self.out_good_label = Label(
            self.frame,
            text=
            """Output File: If you don't want any output file for data passing all filters then clear this cell.
The name for data file will default to _prinseq_good_XXXX where XXXX is random characters.
Enter filename here if you don't want that filename
The file extension will be added automatically (either .fasta, .qual, or .fastq).""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.out_good_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Out Good for PE File Section
        self.var_out_good2 = StringVar()
        self.out_good2 = Entry(
            self.frame, textvariable=self.var_out_good2, width=28)
        self.out_good2.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_good2.set('Output filename for 2nd Good File')
        self.out_good2_label = Label(
            self.frame,
            text=
            """Output File: Enter in second output filename if you wouldn't like the filename to be _prinseq_bad_XXXX
filenames contain additionally "_1", "_1_singletons", "_2", and "_2_singletons" before the file extension
for the paired-end data""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.out_good2_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Out Bad Section
        self.var_out_bad = StringVar()
        self.out_bad = Entry(
            self.frame, textvariable=self.var_out_bad, width=28)
        self.out_bad.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_bad.set('Output filename for Bad')
        self.out_bad_label = Label(
            self.frame,
            text=
            """Output File: If you don't want any output file for data NOT passing any filters then clear this cell.
The name for data file will default to _prinseq_bad_XXXX where XXXX is random characters.
Enter filename here if you don't want that filename.
The file extension will be added automatically (either .fasta, .qual, or .fastq).""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.out_bad_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Out Bad for PE File Section
        self.var_out_bad2 = StringVar()
        self.out_bad2 = Entry(
            self.frame, textvariable=self.var_out_bad2, width=28)
        self.out_bad2.grid(row=x, column=0, padx=5, pady=5)
        self.var_out_bad2.set('Output filename for 2nd Bad File')
        self.out_bad2_label = Label(
            self.frame,
            text=
            """Output File: Enter in second output filename if you wouldn't like the filename to be _prinseq_bad_XXXX
filenames contain additionally "_1", "_1_singletons", "_2", and "_2_singletons" before the file extension
for the paired-end data""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.out_bad2_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Log File Section
        self.var_log = StringVar()
        self.log = Entry(self.frame, textvariable=self.var_log, width=28)
        self.log.grid(row=x, column=0, padx=5, pady=5)
        self.var_log.set('Log Filename')
        self.log_label = Label(
            self.frame,
            text=
            """Log file to keep track of parameters, errors... Must clear cell or input filename to for Log file to be outputted.
Defaults to inputname.log if cell is cleared""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.log_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Graph Data File Section
        self.var_graph_data = StringVar()
        self.graph_data = Entry(
            self.frame, textvariable=self.var_graph_data, width=28)
        self.graph_data.grid(row=x, column=0, padx=5, pady=5)
        self.var_graph_data.set('Graph Data Filename')
        self.graph_data_label = Label(
            self.frame,
            text=
            """File that contains necessary information to generate the graphs similar to ones in the web version. 
If just want only graph data clear cells for Out Good and Out Bad. Must clear cell or input filename for graph data file to be outputted.
When cell is cleared defaults to inputname.gd""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.graph_data_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Input Graph Stats File Section
        self.var_graph_stats = StringVar()
        self.graph_stats = Entry(
            self.frame, textvariable=self.var_graph_stats, width=28)
        self.graph_stats.grid(row=x, column=0, padx=5, pady=5)
        self.var_graph_stats.set('Graph Stats')
        self.graph_stats_label = Label(
            self.frame,
            text=
            """Use this option to select statistics calculated and included in the graph_data file.
Default is all stats. Allowed options(separate multiple by comma with no spaces):
ld(Length distribution), gc(GC content distribution), qd(Base quality distribution), ns(Occurence of N), 
pt(Poly-A/T tails), ts(Tag sequence check), aq(Assembly quality measure), de(Sequence duplication - exact only),
da(Sequence duplication - exact + 5'/3'), sc(Sequence complexity), dn(Dinucleotide odds ratios, 
includes PCA plots)""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.graph_stats_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Qual No Scale Section
        self.var_qual_noscale = IntVar()
        self.qual_noscale = Checkbutton(
            self.frame,
            text="Qual Noscale",
            variable=self.var_qual_noscale,
            width=28,
            bg="white")
        self.qual_noscale.grid(row=x, column=0, padx=5, pady=5)
        self.qual_noscale_label = Label(
            self.frame,
            bg="white",
            text=
            "Use this option if all your sequences are shorter than 100bp and as they do not require to scale quality data to 100 data points in the graph",
            relief=FLAT)
        self.qual_noscale_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Qual No Header Section
        self.var_no_qual_header = IntVar()
        self.no_qual_header = Checkbutton(
            self.frame,
            text="No Qual Header",
            variable=self.var_no_qual_header,
            width=28,
            bg="white")
        self.no_qual_header.grid(row=x, column=0, padx=5, pady=5)
        self.no_qual_header_label = Label(
            self.frame,
            bg="white",
            text=
            "In order to reduce file size, this will generate an empty header line in FASTQ files. Instead of +header, only the + sign will be output.",
            relief=FLAT)
        self.no_qual_header_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Exact Only Section
        self.var_exact_only = IntVar()
        self.exact_only = Checkbutton(
            self.frame,
            text="Exact Duplicates",
            variable=self.var_exact_only,
            width=28,
            bg="white")
        self.exact_only.grid(row=x, column=0, padx=5, pady=5)
        self.exact_only_label = Label(
            self.frame,
            text=
            """Use this option to check for exact (forward and reverse) duplicates only when generating the graph data. 
This keeps the memory requirements low for large input files and is faster""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.exact_only_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Go To Build Filter Section
        self.FILTER(x)

        return

    def FILTER(self, x):

        ##Title of Optional Section
        self.filter_title = Label(
            self.frame, text="Filter Options", relief=RAISED, bg="white")
        self.filter_title.grid(
            row=x, column=0, columnspan=10, padx=5, pady=(5, 30), sticky="we")
        x += 1

        ##Min Length Section
        self.var_min_len = StringVar()
        self.min_len = Entry(
            self.frame, textvariable=self.var_min_len, width=28)
        self.min_len.grid(row=x, column=0, padx=5, pady=5)
        self.var_min_len.set('Min Length: Enter Integer')
        self.min_len_label = Label(
            self.frame,
            text="Filter sequence shorter than min_len. Must plug in integer",
            relief=FLAT,
            bg="white")
        self.min_len_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Max Length Section
        self.var_max_len = StringVar()
        self.max_len = Entry(
            self.frame, textvariable=self.var_max_len, width=28)
        self.max_len.grid(row=x, column=0, padx=5, pady=5)
        self.var_max_len.set('Max Length: Enter Integer')
        self.max_len_label = Label(
            self.frame,
            text="Filter sequence longer than max_len. Must plug in integer",
            relief=FLAT,
            bg="white")
        self.max_len_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Range Length Section
        self.var_range_len = StringVar()
        self.range_len = Entry(
            self.frame, textvariable=self.var_range_len, width=28)
        self.range_len.grid(row=x, column=0, padx=5, pady=5)
        self.var_range_len.set('Length: Enter Range(s)')
        self.range_len_label = Label(
            self.frame,
            bg="white",
            text=
            "Filter sequence by length range. Multiple range values should be separated by comma without spaces. Example: 50-100,250-300",
            relief=FLAT)
        self.range_len_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Min GC Content Section
        self.var_min_gc = StringVar()
        self.min_gc = Entry(self.frame, textvariable=self.var_min_gc, width=28)
        self.min_gc.grid(row=x, column=0, padx=5, pady=5)
        self.var_min_gc.set('Min GC: Enter Integer')
        self.min_gc_label = Label(
            self.frame,
            text=
            "Filter sequence with GC content below min_gc. Must be integer between 0-100",
            relief=FLAT,
            bg="white")
        self.min_gc_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Max GC Content Section
        self.var_max_gc = StringVar()
        self.max_gc = Entry(self.frame, textvariable=self.var_max_gc, width=28)
        self.max_gc.grid(row=x, column=0, padx=5, pady=5)
        self.var_max_gc.set('Max GC: Enter Integer 0-100')
        self.max_gc_label = Label(
            self.frame,
            text=
            "Filter sequence with GC content above max_gc. Must be integer between 0-100",
            relief=FLAT,
            bg="white")
        self.max_gc_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Range GC Content Section
        self.var_range_gc = StringVar()
        self.range_gc = Entry(
            self.frame, textvariable=self.var_range_gc, width=28)
        self.range_gc.grid(row=x, column=0, padx=5, pady=5)
        self.var_range_gc.set('GC: Enter Range(s)')
        self.range_gc_label = Label(
            self.frame,
            text=
            "Filter sequence by GC content range. Multiple range values should be separated by comma without spaces.",
            relief=FLAT,
            bg="white")
        self.range_gc_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Min Qual Score Section
        self.var_min_qual_score = StringVar()
        self.min_qual_score = Entry(
            self.frame, textvariable=self.var_min_qual_score, width=28)
        self.min_qual_score.grid(row=x, column=0, padx=5, pady=5)
        self.var_min_qual_score.set('Min Quality: Enter Integer')
        self.min_qual_score_label = Label(
            self.frame,
            text=
            "Filter sequence with at least one quality score below min_qual_score",
            relief=FLAT,
            bg="white")
        self.min_qual_score_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Max Qual Score Section
        self.var_max_qual_score = StringVar()
        self.max_qual_score = Entry(
            self.frame, textvariable=self.var_max_qual_score, width=28)
        self.max_qual_score.grid(row=x, column=0, padx=5, pady=5)
        self.var_max_qual_score.set('Max Quality: Enter Integer')
        self.max_qual_score_label = Label(
            self.frame,
            text=
            "Filter sequence with at least one quality score above max_qual_score",
            relief=FLAT,
            bg="white")
        self.max_qual_score_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Min Qual Mean Section
        self.var_min_qual_mean = StringVar()
        self.min_qual_mean = Entry(
            self.frame, textvariable=self.var_min_qual_mean, width=28)
        self.min_qual_mean.grid(row=x, column=0, padx=5, pady=5)
        self.var_min_qual_mean.set('Min Qual Mean: Enter Integer')
        self.min_qual_mean_label = Label(
            self.frame,
            text="Filter sequence with quality score mean below min_qual_mean",
            relief=FLAT,
            bg="white")
        self.min_qual_mean_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Max Qual Mean Section
        self.var_max_qual_mean = StringVar()
        self.max_qual_mean = Entry(
            self.frame, textvariable=self.var_max_qual_mean, width=28)
        self.max_qual_mean.grid(row=x, column=0, padx=5, pady=5)
        self.var_max_qual_mean.set('Max Qual Mean: Enter Integer')
        self.max_qual_mean_label = Label(
            self.frame,
            text="Filter sequence with quality score mean above max_qual_mean",
            relief=FLAT,
            bg="white")
        self.max_qual_mean_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##NS Max P Section
        self.var_ns_max_p = StringVar()
        self.ns_max_p = Entry(
            self.frame, textvariable=self.var_ns_max_p, width=28)
        self.ns_max_p.grid(row=x, column=0, padx=5, pady=5)
        self.var_ns_max_p.set('NS_Max_P: Enter Integer 0-100')
        self.ns_max_p_label = Label(
            self.frame,
            text="Filter sequence with more than ns_max_p percentage of Ns",
            relief=FLAT,
            bg="white")
        self.ns_max_p_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##NS Max N Section
        self.var_ns_max_n = StringVar()
        self.ns_max_n = Entry(
            self.frame, textvariable=self.var_ns_max_n, width=28)
        self.ns_max_n.grid(row=x, column=0, padx=5, pady=5)
        self.var_ns_max_n.set('NS_Max_N: Enter Integer')
        self.ns_max_n_label = Label(
            self.frame,
            text="Filter sequence with more than ns_max_n Ns",
            relief=FLAT,
            bg="white")
        self.ns_max_n_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Non IUPAC Section
        self.var_noniupac = IntVar()
        self.noniupac = Checkbutton(
            self.frame,
            text="Non IUPAC",
            variable=self.var_noniupac,
            width=28,
            bg="white")
        self.noniupac.grid(row=x, column=0, padx=5, pady=5)
        self.noniupac_label = Label(
            self.frame,
            text="Filter sequence with characters other than A, C, G, T or N",
            relief=FLAT,
            bg="white")
        self.noniupac_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Seq Num Section
        self.var_seq_num = StringVar()
        self.seq_num = Entry(
            self.frame, textvariable=self.var_seq_num, width=28)
        self.seq_num.grid(row=x, column=0, padx=5, pady=5)
        self.var_seq_num.set('Seq_Num: Enter Integer')
        self.seq_num_label = Label(
            self.frame,
            text=
            "Only keep the first seq_num number of sequences (that pass all other filters)",
            relief=FLAT,
            bg="white")
        self.seq_num_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Derep Section
        self.var_derep = StringVar()
        self.derep = Entry(self.frame, textvariable=self.var_derep, width=28)
        self.derep.grid(row=x, column=0, padx=5, pady=5)
        self.var_derep.set('Duplicates: Enter Integer')
        self.derep_label = Label(
            self.frame,
            text=
            """Type of duplicates to filter. Allowed values are 1, 2, 3, 4 and 5. Use integers for multiple selections (e.g. 124 to use type 1, 2 and 4).
1 (exact duplicate), 2 (5' duplicate), 3 (3' duplicate), 4 (reverse complement exact duplicate), 5 (reverse complement 5'/3' duplicate)""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.derep_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Derep Min Section
        self.var_derep_min = StringVar()
        self.derep_min = Entry(
            self.frame, textvariable=self.var_derep_min, width=28)
        self.derep_min.grid(row=x, column=0, padx=5, pady=5)
        self.var_derep_min.set('Duplicates:Enter Integer 2 or greater')
        self.derep_min_label = Label(
            self.frame,
            text=
            """This option specifies the number of duplicates. If you want to remove sequence duplicates that occur more than x times, 
then you would specify x+1 as the -derep_min values. to remove sequences that occur more than 5 times,
you would specify -derep_min 6. This option can only be used in combination with -derep 1 and/or 4""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.derep_min_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##LC Method Section
        self.var_lc_method = StringVar()
        self.var_lc_method.set("Low Complexity Filter")  # default
        self.lc_method = OptionMenu(self.frame, self.var_lc_method, "dust",
                                    "entropy", "neither")
        self.lc_method.grid(row=x, column=0, padx=5, pady=5)
        self.lc_method_label = Label(
            self.frame,
            text="Method to filter low complexity sequences",
            relief=FLAT,
            bg="white")
        self.lc_method_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##LC Threshold Section
        self.var_lc_threshold = StringVar()
        self.lc_threshold = Entry(
            self.frame, textvariable=self.var_lc_threshold, width=28)
        self.lc_threshold.grid(row=x, column=0, padx=5, pady=5)
        self.var_lc_threshold.set('Enter Integer 0-100')
        self.lc_threshold_label = Label(
            self.frame,
            text=
            """The threshold value used to filter sequences by sequence complexity. 
The dust method uses this as max allowed score and the entropy method as min allowed value.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.lc_threshold_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Custom Parameters Section
        self.var_custom_params = StringVar()
        self.custom_params = Entry(
            self.frame, textvariable=self.var_custom_params, width=28)
        self.custom_params.grid(row=x, column=0, padx=5, pady=5)
        self.var_custom_params.set('Enter Pattern, Repeats or Percentage')
        self.custom_params_label = Label(
            self.frame,
            text=
            """Can be used to specify additional filters. The custom parameters have to be specified within quotes.
Please separate parameter values with a space and separate new parameter sets with semicolon (;). Parameters are defined by two values:
(1) the pattern (any combination of the letters "ACGTN"),
(2) the number of repeats or percentage of occurence
Percentage values are defined by a number followed by the %-sign (without space). If no %-sign is given, 
it is assumed that the given number specifies the number of repeats of the pattern.
Examples: "AAT 10" (filters out sequences containing AATAATAATAATAATAATAATAATAATAAT anywhere in the sequence),
"T 70%" (filters out sequences with more than 70% Ts in the sequence),
"A 15" (filters out sequences containing AAAAAAAAAAAAAAA anywhere in the sequence), "AAT 10;T 70%;A 15" (apply all three filters)""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.custom_params_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Go To Build Trim Section
        self.TRIM(x)
        return

    def TRIM(self, x):

        ##Title of Optional Section
        self.trim_title = Label(
            self.frame, text="Trim Options", relief=RAISED, bg="white")
        self.trim_title.grid(
            row=x, column=0, columnspan=10, padx=5, pady=(5, 30), sticky="we")
        x += 1

        ##Trim to Length Section
        self.var_trim_to_len = StringVar()
        self.trim_to_len = Entry(
            self.frame, textvariable=self.var_trim_to_len, width=28)
        self.trim_to_len.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_to_len.set('Trim to Len: Enter Integer')
        self.trim_to_len_label = Label(
            self.frame,
            text=
            "Trim all sequence from the 3'-end to result in sequence with this length",
            relief=FLAT,
            bg="white")
        self.trim_to_len_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Left Section
        self.var_trim_left = StringVar()
        self.trim_left = Entry(
            self.frame, textvariable=self.var_trim_left, width=28)
        self.trim_left.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_left.set('Trim Left: Enter Integer')
        self.trim_left_label = Label(
            self.frame,
            text="Trim sequence at the 5'-end by trim_left positions",
            relief=FLAT,
            bg="white")
        self.trim_left_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Right Section
        self.var_trim_right = StringVar()
        self.trim_right = Entry(
            self.frame, textvariable=self.var_trim_right, width=28)
        self.trim_right.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_right.set('Trim Right: Enter Integer')
        self.trim_right_label = Label(
            self.frame,
            text="Trim sequence at the 3'-end by trim_right positions",
            relief=FLAT,
            bg="white")
        self.trim_right_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Left P Section
        self.var_trim_left_p = StringVar()
        self.trim_left_p = Entry(
            self.frame, textvariable=self.var_trim_left_p, width=28)
        self.trim_left_p.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_left_p.set('Trim Left %: Enter Integer 0-100')
        self.trim_left_p_label = Label(
            self.frame,
            text=
            """Trim sequence at the 5'-end by trim_left_p percentage of read length. The trim length is rounded towards the lower integer
(e.g. 143.6 is rounded to 143 positions). Use an integer between 1 and 100 for the percentage value.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.trim_left_p_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Right P Section
        self.var_trim_right_p = StringVar()
        self.trim_right_p = Entry(
            self.frame, textvariable=self.var_trim_right_p, width=28)
        self.trim_right_p.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_right_p.set('Trim Right %: Enter Integer 0-100')
        self.trim_right_p_label = Label(
            self.frame,
            text=
            """Trim sequence at the 3'-end by trim_right_p percentage of read length. The trim length is rounded towards the lower integer 
(e.g. 143.6 is rounded to 143 positions). Use an integer between 1 and 100 for the percentage value.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.trim_right_p_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Tail Left Section
        self.var_trim_tail_left = StringVar()
        self.trim_tail_left = Entry(
            self.frame, textvariable=self.var_trim_tail_left, width=28)
        self.trim_tail_left.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_tail_left.set('Trim Left Tail: Enter Integer')
        self.trim_tail_left_label = Label(
            self.frame,
            text=
            "Trim poly-A/T tail with a minimum length of trim_tail_left at the 5'-end",
            relief=FLAT,
            bg="white")
        self.trim_tail_left_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Tail Right Section
        self.var_trim_tail_right = StringVar()
        self.trim_tail_right = Entry(
            self.frame, textvariable=self.var_trim_tail_right, width=28)
        self.trim_tail_right.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_tail_right.set('Trim Right Tail: Enter Integer')
        self.trim_tail_right_label = Label(
            self.frame,
            text=
            "Trim poly-A/T tail with a minimum length of trim_tail_right at the 3'-end",
            relief=FLAT,
            bg="white")
        self.trim_tail_right_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim NS Left Section
        self.var_trim_ns_left = StringVar()
        self.trim_ns_left = Entry(
            self.frame, textvariable=self.var_trim_ns_left, width=28)
        self.trim_ns_left.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_ns_left.set('Trim NS Left: Enter Integer')
        self.trim_ns_left_label = Label(
            self.frame,
            text=
            "Trim poly-N tail with a minimum length of trim_ns_left at the 5'-end",
            relief=FLAT,
            bg="white")
        self.trim_ns_left_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim NS Right Section
        self.var_trim_ns_right = StringVar()
        self.trim_ns_right = Entry(
            self.frame, textvariable=self.var_trim_ns_right, width=28)
        self.trim_ns_right.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_ns_right.set('Trim NS Right: Enter Integer')
        self.trim_ns_right_label = Label(
            self.frame,
            text=
            "Trim poly-N tail with a minimum length of trim_ns_right at the 3'-end",
            relief=FLAT,
            bg="white")
        self.trim_ns_right_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Qual Left Section
        self.var_trim_qual_left = StringVar()
        self.trim_qual_left = Entry(
            self.frame, textvariable=self.var_trim_qual_left, width=28)
        self.trim_qual_left.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_qual_left.set('Trim Qual Left: Enter Integer')
        self.trim_qual_left_label = Label(
            self.frame,
            text=
            "Trim sequence by quality score from the 5'-end with this threshold score",
            relief=FLAT,
            bg="white")
        self.trim_qual_left_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Qual Right Section
        self.var_trim_qual_right = StringVar()
        self.trim_qual_right = Entry(
            self.frame, textvariable=self.var_trim_qual_right, width=28)
        self.trim_qual_right.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_qual_right.set('Trim Qual Right: Enter Integer')
        self.trim_qual_right_label = Label(
            self.frame,
            text=
            "Trim sequence by quality score from the 3'-end with this threshold score",
            relief=FLAT,
            bg="white")
        self.trim_qual_right_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Qual Type Section
        self.var_trim_qual_type = StringVar()
        self.var_trim_qual_type.set("Quality Calculation")  # default
        self.trim_qual_type = OptionMenu(self.frame, self.var_trim_qual_type,
                                         "min", "mean", "max", "sum")
        self.trim_qual_type.grid(row=x, column=0, padx=5, pady=5)
        self.trim_qual_type_label = Label(
            self.frame,
            text="Type of quality score calculation to use. Default = Min",
            relief=FLAT,
            bg="white")
        self.trim_qual_type_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Qual Rule Section
        self.var_trim_qual_rule = StringVar()
        self.var_trim_qual_rule.set("Quality Rule")  # default
        self.trim_qual_rule = OptionMenu(self.frame, self.var_trim_qual_rule,
                                         "Less Than", "Equal To",
                                         "Greater Than")
        self.trim_qual_rule.grid(row=x, column=0, padx=5, pady=5)
        self.trim_qual_rule_label = Label(
            self.frame,
            text=
            "Rule to use to compare quality score to calculated value. Default = Less Than",
            relief=FLAT,
            bg="white")
        self.trim_qual_rule_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Qual Window Section
        self.var_trim_qual_window = StringVar()
        self.trim_qual_window = Entry(
            self.frame, textvariable=self.var_trim_qual_window, width=28)
        self.trim_qual_window.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_qual_window.set('Window Size: Enter Integer')
        self.trim_qual_window_label = Label(
            self.frame,
            text=
            """The sliding window size used to calculate quality score by type. 
To stop at the first base that fails the rule defined, use a window size of 1. Default = 1""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.trim_qual_window_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Trim Qual Step Section
        self.var_trim_qual_step = StringVar()
        self.trim_qual_step = Entry(
            self.frame, textvariable=self.var_trim_qual_step, width=28)
        self.trim_qual_step.grid(row=x, column=0, padx=5, pady=5)
        self.var_trim_qual_step.set('Window Step Size: Enter Integer')
        self.trim_qual_step_label = Label(
            self.frame,
            text=
            """Step size used to move the sliding window. To move the window over all quality scores without missing any,
the step size should be less or equal to the window size.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.trim_qual_step_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Go To Build Reformat Section
        self.REFORMAT(x)
        return

    def REFORMAT(self, x):

        ##Title of Reformat Section
        self.reformat_title = Label(
            self.frame, text="Reformat Options", relief=RAISED, bg="white")
        self.reformat_title.grid(
            row=x, column=0, columnspan=10, padx=5, pady=(5, 30), sticky="we")
        x += 1

        ##Seq Case Section
        self.var_seq_case = StringVar()
        self.var_seq_case.set("Sequence Case")  # default
        self.seq_case = OptionMenu(self.frame, self.var_seq_case, "Upper Case",
                                   "Lower Case")
        self.seq_case.grid(row=x, column=0, padx=5, pady=5)
        self.seq_case_label = Label(
            self.frame,
            text="Changes sequence character case to upper or lower case",
            relief=FLAT,
            bg="white")
        self.seq_case_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##DNA RNA Conversion Section
        self.var_dna_rna = StringVar()
        self.var_dna_rna.set("Sequence Conversion")  # default
        self.dna_rna = OptionMenu(self.frame, self.var_dna_rna, "RNA to DNA",
                                  "DNA to RNA")
        self.dna_rna.grid(row=x, column=0, padx=5, pady=5)
        self.dna_rna_label = Label(
            self.frame,
            text="Convert sequence between DNA and RNA",
            relief=FLAT,
            bg="white")
        self.dna_rna_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Line Width Section
        self.var_line_width = StringVar()
        self.line_width = Entry(
            self.frame, textvariable=self.var_line_width, width=28)
        self.line_width.grid(row=x, column=0, padx=5, pady=5)
        self.var_line_width.set('Line Width: Enter Integer')
        self.line_width_label = Label(
            self.frame,
            text=
            """Sequence characters per line. Use 0 if you want each sequence in a single line.
Use 80 for line breaks every 80 characters. Note that this option only applies to FASTA output files,
since FASTQ files store sequences without additional line breaks""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.line_width_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Remove Header Section
        self.var_rm_header = IntVar()
        self.rm_header = Checkbutton(
            self.frame,
            text="Remove Header",
            variable=self.var_rm_header,
            width=28,
            bg="white")
        self.rm_header.grid(row=x, column=0, padx=5, pady=5)
        self.rm_header_label = Label(
            self.frame,
            text=
            "Remove the sequence header. This includes everything after the sequence identifier (which is kept unchanged)",
            relief=FLAT,
            bg="white")
        self.rm_header_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Seq ID Section
        self.var_seq_id = StringVar()
        self.seq_id = Entry(self.frame, textvariable=self.var_seq_id, width=28)
        self.seq_id.grid(row=x, column=0, padx=5, pady=5)
        self.var_seq_id.set('Sequence Identifier')
        self.seq_id_label = Label(
            self.frame,
            text=
            "Rename the sequence identifier. A counter is added to each identifier to assure its uniqueness",
            relief=FLAT,
            bg="white")
        self.seq_id_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Go To Build Summary Statistic Section
        self.SUMMARY_STATISTIC(x)

        return

    def SUMMARY_STATISTIC(self, x):

        ##Title of Summary Statistic Section
        self.summary_statistic_title = Label(
            self.frame, text="Statistic Options", relief=RAISED, bg="white")
        self.summary_statistic_title.grid(
            row=x, column=0, columnspan=10, padx=5, pady=(5, 30), sticky="we")
        x += 1

        ##Output All Stats Section
        self.var_stats_all = IntVar()
        self.stats_all = Checkbutton(
            self.frame,
            text="Output All",
            variable=self.var_stats_all,
            width=28,
            bg="white")
        self.stats_all.grid(row=x, column=0, padx=5, pady=5)
        self.stats_all_label = Label(
            self.frame,
            text="Outputs all available summary statistics.",
            relief=FLAT,
            bg="white")
        self.stats_all_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output Stats Info Section
        self.var_stats_info = IntVar()
        self.stats_info = Checkbutton(
            self.frame,
            text="Stats Information",
            variable=self.var_stats_info,
            width=28,
            bg="white")
        self.stats_info.grid(row=x, column=0, padx=5, pady=5)
        self.stats_info_label = Label(
            self.frame,
            text=
            "Outputs basic information such as number of reads (reads) and total bases (bases).",
            relief=FLAT,
            bg="white")
        self.stats_info_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output Stats Length Section
        self.var_stats_len = IntVar()
        self.stats_len = Checkbutton(
            self.frame,
            text="Stats Length",
            variable=self.var_stats_len,
            width=28,
            bg="white")
        self.stats_len.grid(row=x, column=0, padx=5, pady=5)
        self.stats_len_label = Label(
            self.frame,
            text=
            "Outputs minimum, maximum, range, mean, standard deviation, mode and mode value, and median for read length.",
            relief=FLAT,
            bg="white")
        self.stats_len_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output Dinucleotide Stats Section
        self.var_stats_dinuc = IntVar()
        self.stats_dinuc = Checkbutton(
            self.frame,
            text="Dinucleotide Odds Ratio",
            variable=self.var_stats_dinuc,
            width=28,
            bg="white")
        self.stats_dinuc.grid(row=x, column=0, padx=5, pady=5)
        self.stats_dinuc_label = Label(
            self.frame,
            text=
            """Outputs the dinucleotide odds ratio for AA/TT (aatt), AC/GT (acgt), AG/CT (agct), AT (at), CA/TG (catg), CC/GG (ccgg),
CG (cg), GA/TC (gatc), GC (gc) and TA (ta).""",
            relief=FLAT,
            bg="white")
        self.stats_dinuc_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output Tag Stats Section
        self.var_stats_tag = IntVar()
        self.stats_tag = Checkbutton(
            self.frame,
            text="Tag Sequence Percent",
            variable=self.var_stats_tag,
            width=28,
            bg="white")
        self.stats_tag.grid(row=x, column=0, padx=5, pady=5)
        self.stats_tag_label = Label(
            self.frame,
            text=
            """Outputs the probability of a tag sequence at the 5'-end (prob5) and 3'-end (prob3) in percentage (0..100).
Provides the number of predefined MIDs (midnum) and the MID sequences 
(midseq, separated by comma, only provided if midnum > 0) that occur in more than 34/100 (approx. 3%) of the reads.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.stats_tag_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output Duplicate Stats Section
        self.var_stats_dupl = IntVar()
        self.stats_dupl = Checkbutton(
            self.frame,
            text="Number of Duplicates",
            variable=self.var_stats_dupl,
            width=28,
            bg="white")
        self.stats_dupl.grid(row=x, column=0, padx=5, pady=5)
        self.stats_dupl_label = Label(
            self.frame,
            text=
            """Outputs the number of exact duplicates (exact), 5' duplicates (5), 3' duplicates (3), 
exact duplicates with reverse complements (exactrevcom) and 5'/3' duplicates with reverse complements (revcomp),
and total number of duplicates (total). The maximum number of duplicates is given under the value name 
with an additional "maxd" (e.g. exactmaxd or 5maxd).""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.stats_dupl_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output NS Stats Section
        self.var_stats_ns = IntVar()
        self.stats_ns = Checkbutton(
            self.frame,
            text="Seqswithn, Maxn, Maxp",
            variable=self.var_stats_ns,
            width=28,
            bg="white")
        self.stats_ns.grid(row=x, column=0, padx=5, pady=5)
        self.stats_ns_label = Label(
            self.frame,
            text=
            """Outputs the number of reads with ambiguous base N (seqswithn), the maximum number of Ns per read (maxn)
and the maximum percentage of Ns per read (maxp). The maxn and maxp value are not necessary from the same sequence.""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.stats_ns_label.grid(row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Output Assembly Stats Section
        self.var_stats_assembly = IntVar()
        self.stats_assembly = Checkbutton(
            self.frame,
            text="N50, N90, etc contig sizes",
            variable=self.var_stats_assembly,
            width=28,
            bg="white")
        self.stats_assembly.grid(row=x, column=0, padx=5, pady=5)
        self.stats_assembly_label = Label(
            self.frame,
            text=
            """Outputs the N50, N90, etc contig sizes. The Nxx contig size is a weighted median that is defined as the length
of the smallest contig C in the sorted list of all contigs where the cumulative length from the largest contig to contig C
is at least xx% of the total length (sum of contig lengths).""",
            relief=FLAT,
            justify=LEFT,
            bg="white")
        self.stats_assembly_label.grid(
            row=x, column=1, padx=5, pady=5, sticky="w")
        x += 1

        ##Go To Options Section
        self.OPTIONS(x)
        return

    def FILE_TYPE(self, x):

        ##Depending on the type of file, The program will display the necessary Single end or paired end options
        ##Then will display button as well
        if (self.var_file_type.get() == "Fastq File"
                or self.var_file_type.get() == "Amino Acid File"
                or self.var_file_type.get() == "Fasta File"):
            self.browse_file1.grid()
            self.label_filename.grid()
            self.browse_file2.grid_remove()
            self.label_filename2.grid_remove()
            self.label_filename.config(
                text=
                'Input File. Avoid spaces with folder names as this can cause errors.'
            )
            self.out_good2.grid_remove()
            self.out_bad2.grid_remove()
            self.out_bad2_label.grid_remove()
            self.out_good2_label.grid_remove()
        else:
            self.browse_file1.grid()
            self.label_filename.grid()
            self.browse_file2.grid()
            self.label_filename2.grid()
            self.label_filename.config(text='Input Paired End File')
            if (self.var_options.get() == "Output Options"):
                self.out_good2.grid()
                self.out_bad2.grid()
                self.out_bad2_label.grid()
                self.out_good2_label.grid()
        if (self.var_file_type.get() == "Fastq File"
                or self.var_file_type.get() == "Paired-end Fastq File"):
            self.phred_button.grid()
            self.phred_lab.grid()
        else:
            self.phred_button.grid_remove()
            self.phred_lab.grid_remove()

        self.run_button.grid()
        return

    def OPTIONS(self, x):

        ##When creating the display it will remove all options from the screen initially, however when an option
        ##is picked to change, it will display those specific options to change

        self.output_title.grid_remove()
        self.o_format.grid_remove()
        self.o_format_label.grid_remove()
        self.out_good.grid_remove()
        self.out_good2.grid_remove()
        self.out_bad2.grid_remove()
        self.out_bad2_label.grid_remove()
        self.out_good_label.grid_remove()
        self.out_bad.grid_remove()
        self.out_bad_label.grid_remove()
        self.log.grid_remove()
        self.log_label.grid_remove()
        self.out_good2_label.grid_remove()
        self.graph_data.grid_remove()
        self.graph_data_label.grid_remove()
        self.graph_stats.grid_remove()
        self.graph_stats_label.grid_remove()
        self.qual_noscale.grid_remove()
        self.qual_noscale_label.grid_remove()
        self.no_qual_header.grid_remove()
        self.no_qual_header_label.grid_remove()
        self.exact_only.grid_remove()
        self.exact_only_label.grid_remove()

        self.filter_title.grid_remove()
        self.min_len.grid_remove()
        self.min_len_label.grid_remove()
        self.max_len.grid_remove()
        self.max_len_label.grid_remove()
        self.range_len.grid_remove()
        self.range_len_label.grid_remove()
        self.min_gc.grid_remove()
        self.min_gc_label.grid_remove()
        self.max_gc.grid_remove()
        self.max_gc_label.grid_remove()
        self.range_gc.grid_remove()
        self.range_gc_label.grid_remove()
        self.min_qual_score.grid_remove()
        self.min_qual_score_label.grid_remove()
        self.max_qual_score.grid_remove()
        self.max_qual_score_label.grid_remove()
        self.ns_max_p.grid_remove()
        self.ns_max_p_label.grid_remove()
        self.ns_max_n.grid_remove()
        self.ns_max_n_label.grid_remove()
        self.noniupac.grid_remove()
        self.noniupac_label.grid_remove()
        self.seq_num.grid_remove()
        self.seq_num_label.grid_remove()
        self.derep.grid_remove()
        self.derep_label.grid_remove()
        self.derep_min.grid_remove()
        self.derep_min_label.grid_remove()
        self.lc_method.grid_remove()
        self.lc_method_label.grid_remove()
        self.lc_threshold.grid_remove()
        self.lc_threshold_label.grid_remove()
        self.custom_params.grid_remove()
        self.custom_params_label.grid_remove()
        self.min_qual_mean.grid_remove()
        self.min_qual_mean_label.grid_remove()
        self.max_qual_mean.grid_remove()
        self.max_qual_mean_label.grid_remove()

        self.trim_title.grid_remove()
        self.trim_to_len.grid_remove()
        self.trim_to_len_label.grid_remove()
        self.trim_left.grid_remove()
        self.trim_left_label.grid_remove()
        self.trim_right.grid_remove()
        self.trim_right_label.grid_remove()
        self.trim_left_p.grid_remove()
        self.trim_left_p_label.grid_remove()
        self.trim_right_p.grid_remove()
        self.trim_right_p_label.grid_remove()
        self.trim_tail_left.grid_remove()
        self.trim_tail_left_label.grid_remove()
        self.trim_tail_right.grid_remove()
        self.trim_tail_right_label.grid_remove()
        self.trim_ns_left.grid_remove()
        self.trim_ns_left_label.grid_remove()
        self.trim_ns_right.grid_remove()
        self.trim_ns_right_label.grid_remove()
        self.trim_qual_left.grid_remove()
        self.trim_qual_left_label.grid_remove()
        self.trim_qual_right.grid_remove()
        self.trim_qual_right_label.grid_remove()
        self.trim_qual_type.grid_remove()
        self.trim_qual_type_label.grid_remove()
        self.trim_qual_rule.grid_remove()
        self.trim_qual_rule_label.grid_remove()
        self.trim_qual_window.grid_remove()
        self.trim_qual_window_label.grid_remove()
        self.trim_qual_step.grid_remove()
        self.trim_qual_step_label.grid_remove()

        self.reformat_title.grid_remove()
        self.seq_case.grid_remove()
        self.seq_case_label.grid_remove()
        self.dna_rna.grid_remove()
        self.dna_rna_label.grid_remove()
        self.line_width.grid_remove()
        self.line_width_label.grid_remove()
        self.rm_header.grid_remove()
        self.rm_header_label.grid_remove()
        self.seq_id.grid_remove()
        self.seq_id_label.grid_remove()

        self.summary_statistic_title.grid_remove()
        self.stats_all.grid_remove()
        self.stats_all_label.grid_remove()
        self.stats_info.grid_remove()
        self.stats_info_label.grid_remove()
        self.stats_len.grid_remove()
        self.stats_len_label.grid_remove()
        self.stats_dinuc.grid_remove()
        self.stats_dinuc_label.grid_remove()
        self.stats_tag.grid_remove()
        self.stats_tag_label.grid_remove()
        self.stats_dupl.grid_remove()
        self.stats_dupl_label.grid_remove()
        self.stats_ns.grid_remove()
        self.stats_ns_label.grid_remove()
        self.stats_assembly.grid_remove()
        self.stats_assembly_label.grid_remove()

        if (self.var_options.get() == "Output Options"):

            self.output_title.grid()
            self.o_format.grid()
            self.o_format_label.grid()
            self.out_good.grid()
            self.out_good_label.grid()
            self.out_bad.grid()
            self.out_bad_label.grid()
            self.log.grid()
            self.log_label.grid()
            self.graph_data.grid()
            self.graph_data_label.grid()
            self.graph_stats.grid()
            self.graph_stats_label.grid()
            self.qual_noscale.grid()
            self.qual_noscale_label.grid()
            self.no_qual_header.grid()
            self.no_qual_header_label.grid()
            self.exact_only.grid()
            self.exact_only_label.grid()

            if (self.var_file_type.get() == "Paired-end Fastq File"
                    or self.var_file_type.get() == "Paired-end Fasta File"):
                self.out_good2.grid()
                self.out_bad2.grid()
                self.out_bad2_label.grid()
                self.out_good2_label.grid()
            else:
                self.out_good2.grid_remove()
                self.out_bad2.grid_remove()
                self.out_bad2_label.grid_remove()
                self.out_good2_label.grid_remove()

        elif (self.var_options.get() == "Filter Options"):

            self.filter_title.grid()
            self.min_len.grid()
            self.min_len_label.grid()
            self.max_len.grid()
            self.max_len_label.grid()
            self.range_len.grid()
            self.range_len_label.grid()
            self.min_gc.grid()
            self.min_gc_label.grid()
            self.max_gc.grid()
            self.max_gc_label.grid()
            self.range_gc.grid()
            self.range_gc_label.grid()
            self.min_qual_score.grid()
            self.min_qual_score_label.grid()
            self.max_qual_score.grid()
            self.max_qual_score_label.grid()
            self.ns_max_p.grid()
            self.ns_max_p_label.grid()
            self.ns_max_n.grid()
            self.ns_max_n_label.grid()
            self.noniupac.grid()
            self.noniupac_label.grid()
            self.seq_num.grid()
            self.seq_num_label.grid()
            self.derep.grid()
            self.derep_label.grid()
            self.derep_min.grid()
            self.derep_min_label.grid()
            self.lc_method.grid()
            self.lc_method_label.grid()
            self.lc_threshold.grid()
            self.lc_threshold_label.grid()
            self.custom_params.grid()
            self.custom_params_label.grid()
            self.min_qual_mean.grid()
            self.min_qual_mean_label.grid()
            self.max_qual_mean.grid()
            self.max_qual_mean_label.grid()

        elif (self.var_options.get() == "Trim Options"):

            self.trim_title.grid()
            self.trim_to_len.grid()
            self.trim_to_len_label.grid()
            self.trim_left.grid()
            self.trim_left_label.grid()
            self.trim_right.grid()
            self.trim_right_label.grid()
            self.trim_left_p.grid()
            self.trim_left_p_label.grid()
            self.trim_right_p.grid()
            self.trim_right_p_label.grid()
            self.trim_tail_left.grid()
            self.trim_tail_left_label.grid()
            self.trim_tail_right.grid()
            self.trim_tail_right_label.grid()
            self.trim_ns_left.grid()
            self.trim_ns_left_label.grid()
            self.trim_ns_right.grid()
            self.trim_ns_right_label.grid()
            self.trim_qual_left.grid()
            self.trim_qual_left_label.grid()
            self.trim_qual_right.grid()
            self.trim_qual_right_label.grid()
            self.trim_qual_type.grid()
            self.trim_qual_type_label.grid()
            self.trim_qual_rule.grid()
            self.trim_qual_rule_label.grid()
            self.trim_qual_window.grid()
            self.trim_qual_window_label.grid()
            self.trim_qual_step.grid()
            self.trim_qual_step_label.grid()

        elif (self.var_options.get() == "Reformat Options"):

            self.reformat_title.grid()
            self.seq_case.grid()
            self.seq_case_label.grid()
            self.dna_rna.grid()
            self.dna_rna_label.grid()
            self.line_width.grid()
            self.line_width_label.grid()
            self.rm_header.grid()
            self.rm_header_label.grid()
            self.seq_id.grid()
            self.seq_id_label.grid()

        elif (self.var_options.get() == "Summary Statistic Options"):

            self.summary_statistic_title.grid()
            self.stats_all.grid()
            self.stats_all_label.grid()
            self.stats_info.grid()
            self.stats_info_label.grid()
            self.stats_len.grid()
            self.stats_len_label.grid()
            self.stats_dinuc.grid()
            self.stats_dinuc_label.grid()
            self.stats_tag.grid()
            self.stats_tag_label.grid()
            self.stats_dupl.grid()
            self.stats_dupl_label.grid()
            self.stats_ns.grid()
            self.stats_ns_label.grid()
            self.stats_assembly.grid()
            self.stats_assembly_label.grid()

        return

    def Check_Options(self):

        ##Looks at the options that have been checked off and creates a string##
        ##Set the start of the string
        functions.globstring = "perl ./GenCoF-master/Prinseq/prinseq-lite-0.20.4/prinseq-lite.pl "
        ##Set errors to nothing
        ##If errors present add on string of errors
        errors = ''

        ##Runs through all the options and creates string for the options that have been marked by the user##
        ##If mandatory options not checked or wrong input to an option then add to errors##

        if (self.var_file_type.get() == "Fastq File"):
            if (self.var_filename != ''):
                functions.globstring += (
                    "-fastq " + "'" + self.var_filename + "'" + " ")
            else:
                errors += "Input file not given\n"
            if (self.var_phred.get()):
                functions.globstring += ("-phred64 ")
        elif (self.var_file_type.get() == "Fasta File"):
            if (self.var_filename != ''):
                functions.globstring += (
                    "-fasta " + "'" + self.var_filename + "'" + " ")
            else:
                errors += "Input file not given\n"
        elif (self.var_file_type.get() == "Amino Acid File"):
            if (self.var_filename != ''):
                functions.globstring += (
                    "-aa " + "'" + self.var_filename + "'" + " ")
            else:
                errors += "Input file not given\n"
        elif (self.var_file_type.get() == "Paired-end Fastq File"):
            if (self.var_filename != '' and self.var_paired_file != ''):
                functions.globstring += (
                    "-fastq2 " + "'" + self.var_filename + "'" + " '" +
                    self.var_paired_file + "'")
            else:
                errors += "Input files not given\n"
            if (self.var_phred.get()):
                functions.globstring += ("-phred64 ")
        elif (self.var_file_type.get() == "Paired-end Fasta File"):
            if (self.var_filename != '' and self.var_paired_file != ''):
                functions.globstring += (
                    "-fasta2 " + "'" + self.var_filename + "'" + " '" +
                    self.var_paired_file + "'")
            else:
                errors += "Input files not given\n"
        else:
            errors += "Input file type"

        if (self.out_format.get() == "FASTA only"):
            functions.globstring += ("-out_format " + "1 ")
        elif (self.out_format.get() == "FASTQ"):
            functions.globstring += ("-out_format " + "3 ")
        elif (self.out_format.get() == "FASTA and QUAL"):
            functions.globstring += ("-out_format " + "2 ")
        elif (self.out_format.get() == "FASTQ and FASTA"):
            functions.globstring += ("-out_format " + "4 ")
        elif (self.out_format.get() == "FASTQ, FASTA and QUAL"):
            functions.globstring += ("-out_format " + "5 ")

        if (self.var_file_type.get() != "Paired-end Fastq File"
                and self.var_file_type.get() != "Paired-end Fasta File"):
            if (self.var_out_good.get() == ''):
                functions.globstring += ("-out_good null ")
            elif (self.var_out_good.get() != 'Output filename for Good'):
                functions.globstring += (
                    "-out_good " + self.var_out_good.get() + ' ')
            if (self.var_out_bad.get() == ''):
                functions.globstring += ("-out_bad null ")
            elif (self.var_out_bad.get() != 'Output filename for Bad'):
                functions.globstring += (
                    "-out_bad " + self.var_out_bad.get() + ' ')
        else:
            if (self.var_out_good.get() == ''):
                functions.globstring += ("-out_good null ")
            elif (self.var_out_good.get() != 'Output filename for Good'
                  and self.var_out_good2.get() !=
                  'Output filename for 2nd Good File'):
                functions.globstring += (
                    "-out_good " + self.var_out_good.get() + ' ' +
                    self.var_out_good2.get() + ' ')
            if (self.var_out_bad.get() == ''):
                functions.globstring += ("-out_bad null ")
            elif (self.var_out_bad.get() != 'Output filename for Bad'
                  and self.var_out_bad2.get() !=
                  'Output filename for 2nd Bad File'):
                functions.globstring += ("-out_bad " + self.var_out_bad.get() +
                                         ' ' + self.var_out_bad2.get() + ' ')

        if (self.var_log.get() == ''):
            functions.globstring += ("-log ")
        elif (self.var_log.get() != 'Log Filename'):
            functions.globstring += ("-log " + self.var_log.get() + " ")
        if (self.var_graph_data.get() == ''):
            functions.globstring += ("-graph_data ")
        elif (self.var_graph_data.get() != 'Graph Data Filename'):
            functions.globstring += (
                "-graph_data " + self.var_graph_data.get() + " ")
        if (self.var_graph_stats.get() != 'Graph Stats'
                and self.var_graph_stats.get() != ''):
            functions.globstring += (
                "-graph_stats " + self.var_graph_stats.get() + " ")
        if (self.var_qual_noscale.get()):
            functions.globstring += ("-qual_noscale ")
        if (self.var_no_qual_header.get()):
            functions.globstring += ("-no_qual_header ")
        if (self.var_exact_only.get()):
            functions.globstring += ("-exact_only ")

        ##Filter Options##
        if (functions.is_int(self.var_min_len.get())):
            functions.globstring += (
                "-min_len " + self.var_min_len.get() + " ")
        if (functions.is_int(self.var_max_len.get())):
            functions.globstring += (
                "-max_len " + self.var_max_len.get() + " ")
        if (self.var_range_len.get() != ''
                and self.var_range_len.get() != 'Length: Enter Range(s)'):
            functions.globstring += (
                "-range_len " + self.var_range_len.get() + " ")
        if (functions.is_int(self.var_min_gc.get())):
            functions.globstring += ("-min_gc " + self.var_min_gc.get() + " ")
        if (functions.is_int(self.var_max_gc.get())):
            functions.globstring += ("-max_gc " + self.var_max_gc.get() + " ")
        if (self.var_range_gc.get() != ''
                and self.var_range_gc.get() != 'GC: Enter Range(s)'):
            functions.globstring += (
                "-range_gc " + self.var_range_gc.get() + " ")
        if (functions.is_int(self.var_min_qual_score.get())):
            functions.globstring += (
                "-min_qual_score " + self.var_min_qual_score.get() + " ")
        if (functions.is_int(self.var_max_qual_score.get())):
            functions.globstring += (
                "-max_qual_score " + self.var_max_qual_score.get() + " ")
        if (functions.is_int(self.var_min_qual_mean.get())):
            functions.globstring += (
                "-min_qual_mean " + self.var_min_qual_mean.get() + " ")
        if (functions.is_int(self.var_max_qual_mean.get())):
            functions.globstring += (
                "-max_qual_mean " + self.var_max_qual_mean.get() + " ")
        if (functions.is_int(self.var_ns_max_p.get())):
            functions.globstring += (
                "-ns_max_p " + self.var_ns_max_p.get() + " ")
        if (functions.is_int(self.var_ns_max_n.get())):
            functions.globstring += (
                "-ns_max_n " + self.var_ns_max_n.get() + " ")
        if (self.var_noniupac.get()):
            functions.globstring += ("-noniupac ")
        if (functions.is_int(self.var_seq_num.get())):
            functions.globstring += (
                "-seq_num " + self.var_seq_num.get() + " ")
        if (functions.is_int(self.var_derep.get())):
            functions.globstring += ("-derep " + self.var_derep.get() + " ")
        if (functions.is_int(self.var_derep_min.get())):
            functions.globstring += (
                "-derep_min " + self.var_derep_min.get() + " ")
        if (self.var_lc_method.get() != "neither"
                and self.var_lc_method.get() != 'Low Complexity Filter'):
            functions.globstring += (
                "-lc_method " + self.var_lc_method.get() + " ")
        if (functions.is_int(self.var_lc_threshold.get())):
            functions.globstring += (
                "-lc_threshold " + self.var_lc_threshold.get() + " ")
        if (self.var_custom_params.get() !=
                'Enter Pattern, Repeats or Percentage'
                and self.var_custom_params.get() != ''):
            functions.globstring += (
                "-custom_params " + self.var_custom_params.get() + " ")

        ##Trim Options##
        if (functions.is_int(self.var_trim_to_len.get())):
            functions.globstring += (
                "-trim_to_len " + self.var_trim_to_len.get() + " ")
        if (functions.is_int(self.var_trim_left.get())):
            functions.globstring += (
                "-trim_left " + self.var_trim_left.get() + " ")
        if (functions.is_int(self.var_trim_right.get())):
            functions.globstring += (
                "-trim_right " + self.var_trim_right.get() + " ")
        if (functions.is_int(self.var_trim_left_p.get())):
            functions.globstring += (
                "-trim_left_p " + self.var_trim_left_p.get() + " ")
        if (functions.is_int(self.var_trim_right_p.get())):
            functions.globstring += (
                "-trim_right_p " + self.var_trim_right_p.get() + " ")
        if (functions.is_int(self.var_trim_tail_left.get())):
            functions.globstring += (
                "-trim_tail_left " + self.var_trim_tail_left.get() + " ")
        if (functions.is_int(self.var_trim_tail_right.get())):
            functions.globstring += (
                "-trim_tail_right " + self.var_trim_tail_right.get() + " ")
        if (functions.is_int(self.var_trim_ns_left.get())):
            functions.globstring += (
                "-trim_ns_left " + self.var_trim_ns_left.get() + " ")
        if (functions.is_int(self.var_trim_ns_right.get())):
            functions.globstring += (
                "-trim_ns_right " + self.var_trim_ns_right.get() + " ")
        if (functions.is_int(self.var_trim_qual_left.get())):
            functions.globstring += (
                "-trim_qual_left " + self.var_trim_qual_left.get() + " ")
        if (functions.is_int(self.var_trim_qual_right.get())):
            functions.globstring += (
                "-trim_qual_right " + self.var_trim_qual_right.get() + " ")
        if (self.var_trim_qual_type.get() != "Quality Calculation"):
            functions.globstring += (
                "-trim_qual_type " + self.var_trim_qual_type.get() + " ")
        if (self.var_trim_qual_rule.get() == "Equal To"):
            functions.globstring += ("-trim_qual_type " + "et ")
        elif (self.var_trim_qual_rule.get() == "Greater Than"):
            functions.globstring += ("-trim_qual_type " + "gt ")
        if (functions.is_int(self.var_trim_qual_window.get())):
            functions.globstring += (
                "-trim_qual_window " + self.var_trim_qual_window.get() + " ")
        if (functions.is_int(self.var_trim_qual_step.get())):
            functions.globstring += (
                "-trim_qual_step " + self.var_trim_qual_step.get() + " ")

        ##Reformat Options##
        if (self.var_seq_case.get() == "Upper Case"):
            functions.globstring += ("-seq_case " + "upper ")
        elif (self.var_seq_case.get() == "Lower Case"):
            functions.globstring += ("-seq_case " + "lower ")
        if (self.var_dna_rna.get() == "RNA to DNA"):
            functions.globstring += ("-dna_rna " + "dna ")
        elif (self.var_dna_rna.get() == "DNA to RNA"):
            functions.globstring += ("-dna_rna " + "rna ")
        if (functions.is_int(self.var_line_width.get())):
            functions.globstring += (
                "-line_width " + self.var_line_width.get() + " ")
        if (self.var_rm_header.get()):
            functions.globstring += ("-rm_header ")
        if (self.var_seq_id.get() != 'Sequence Identifier'
                and self.var_seq_id.get() != ''):
            functions.globstring += ("-seq_id " + self.var_seq_id.get() + " ")

        ##Summary Statistic Options##
        if (self.var_stats_all.get()):
            functions.globstring += ("-stats_all ")
        else:
            if (self.var_stats_info.get()):
                functions.globstring += ("-stats_info ")
            if (self.var_stats_len.get()):
                functions.globstring += ("-stats_len ")
            if (self.var_stats_dinuc.get()):
                functions.globstring += ("-stats_dinuc ")
            if (self.var_stats_tag.get()):
                functions.globstring += ("-stats_tag ")
            if (self.var_stats_dupl.get()):
                functions.globstring += ("-stats_dupl ")
            if (self.var_stats_ns.get()):
                functions.globstring += ("-stats_ns ")
            if (self.var_stats_assembly.get()):
                functions.globstring += ("-stats_assembly ")

        ##If there are no errors than run the string with Prinseq
        ##Put the Output to the Screen from the program run
        ##If there are errors put them to the screen
        self.err_message.config(text="Running....", font="Times 18")
        self.update()
        if (errors == ''):
            cmd_line = shlex.split(functions.globstring)
            if ('prinseq-lite.pl' in os.listdir(
                    './GenCoF-master/Prinseq/prinseq-lite-0.20.4/')):
                p = subprocess.Popen(
                    cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result, error = p.communicate()
                if (error.decode('utf-8') == ''):
                    self.err_message.config(
                        text="OUTPUT: \n" + result.decode('utf-8'),
                        font="Times 18")
                else:
                    self.err_message.config(
                        text='\n' + error.decode('utf-8'),
                        font="Times 18",
                        fg='dark red')
            else:
                self.err_message.config(
                    text="ERRORS: \n Prinseq not in correct directory",
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

    ##Gives ability to Browse for a file and sets to a variable
    def browse_file_input2(self):
        self.var_paired_file = filedialog.askopenfilename()
        return

    def onFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return


if __name__ == "__main__":
    ##Start of App
    ##Creates Window and goes to the Mainloop of the class and creates the App
    root = Tk()
    root.wm_title("PRINSEQ")
    root.geometry('1050x535')
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

#graph data
