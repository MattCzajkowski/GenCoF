import functions, sys, shlex, subprocess, os
from tkinter import filedialog
from tkinter import *

#Specifications: Requires C compiler and Python 3 module Tkinter

##Closes window and opens window run
def Run():	
	root.destroy()
	if(sys.platform == 'linux'):
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
		self.canvas = Canvas(root, borderwidth=0, background="white")
		self.frame = Frame(self.canvas, background="#ffffff")
		self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)

		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")

		self.frame.bind("<Configure>", self.onFrameConfigure)

		##Go To Build Mandatory Section
		self.MANDATORY()
		return

	def MANDATORY(self):
		
		x = 0 #current row for grid
		
		##Returns to run where you can select another module of the GUI
		self.run_butt = Button(self.frame, text="BACK", command=Run)
		self.run_butt.grid(row=x,column=0, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Title of Deconseq Portion of GUI##
		self.file1_title = Label(self.frame, text="Sickle", font="Times 24 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = (5,5), sticky = "we")
		x += 1

		##Title for Mandatory Section
		self.fill_mandat = Label(self.frame, text="""Citation: Joshi NA, Fass JN. (2011). Sickle: A sliding-window, adaptive, quality-based trimming tool for FastQ files 
(Version 1.33) [Software].  Available at https://github.com/najoshi/sickle.""", font="Times 11 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = 5, sticky = "we")
		x += 1

		##Title for Mandatory Section
		self.fill_mandat = Label(self.frame, text="***Must fill all MANDATORY sections***", relief=FLAT, font="Times 20 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = 5, sticky = "we")
		x += 1

		##PE or SE option
		self.var_se_pe = StringVar()
		self.var_se_pe.set("Pick SE or PE       ")
		self.SE_PE = OptionMenu(self.frame, self.var_se_pe, "Single-end            ", "Paired-end", command=self.SE_and_PE)
		self.SE_PE.grid(row = x, column = 0, padx = 5, pady = 5)
		Label(self.frame, text="MANDATORY: single-end or paired-end sequence trimming", relief=FLAT, bg="white").grid(row = x, column = 1, padx = 5, pady = 5, sticky = "w")
		x += 1
		
		##Quality Value option
		self.var_qual = StringVar()
		self.var_qual.set("Pick Quality Type")
		self.Qual = OptionMenu(self.frame, self.var_qual, "Solexa                ", "Illumina", "Sanger").grid(row = x, column = 0, padx = 5, pady = 5)
		Label(self.frame, text="MANDATORY: Type of quality values ", relief=FLAT, bg="white").grid(row = x, column = 1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Input Filename option
		self.var_filename = ''
		self.browse_file1 = Button(self.frame, text="Browse", command=self.browse_file_input1, width=15)
		self.browse_file1.grid(row = x, column = 0, padx = 5, pady = 5)
		self.label_filename = Label(self.frame, text="MANDATORY: Input File: Input filename with .fastq or .fq at end", relief=FLAT, bg="white")
		self.label_filename.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##If PE, Reverse Input Filename
		self.var_reverse_file = ''
		self.browse_file2 = Button(self.frame, text="Browse", command=self.browse_file_input2, width=15)
		self.browse_file2.grid(row = x, column = 0, padx = 5, pady = (5,60))
		self.label_reverse = Label(self.frame, text="MANDATORY IF: you have separate files for forward and reverse reads, input reverse filename", relief=FLAT, bg="white")
		self.label_reverse.grid(row=x,column=1, padx = 5, pady = (5,60), sticky = "w")
		x += 1
		self.browse_file2.grid_remove()# only added when PE is checked
		self.label_reverse.grid_remove()

		#Pick Options to Change Section
		self.var_options = StringVar()
		self.var_options.set("Display Options") # default
		self.options = OptionMenu(self.frame, self.var_options, "Display", "Hide", command=self.OPTIONS)
		self.options.grid(row = x, column = 0, padx = 5, pady = 5)
		Label(self.frame, text="Pick Options To Change Or Leave As Default", relief=FLAT, bg="white").grid(row = x, column = 1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Run Button which goes to function: Check_Options when clicked
		self.run_button = Button(self.frame, text="Run Sickle", command=self.Check_Options)
		self.run_button.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Go To Build Optional Section
		self.OPTIONAL(x)
		return

		
	def OPTIONAL(self, x):

		##Title for Optional Section
		self.label_L = Label(self.frame, text="**OPTIONAL SECTION**", relief=FLAT, font="Times 20 bold", bg="white")
		self.label_L.grid(row=x,column=0, columnspan=10, padx = 5, pady=5, sticky = "we")
		x += 1

		##Output Filename Section
		self.var_out_file = StringVar()
		self.out_file = Entry(self.frame, textvariable = self.var_out_file, width=29)
		self.out_file.grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_out_file.set('Output Filename')
		self.out_file_lab = Label(self.frame, text="OPTIONAL: Output File: Will default to TRIMMED_OUTPUT.fastq", relief=FLAT, bg="white")
		self.out_file_lab.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1		

		##If PE, Reverse Output Filename
		self.var_reverse_output = StringVar()
		self.reverse_out = Entry(self.frame, textvariable = self.var_reverse_output, width=29)
		self.reverse_out.grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_reverse_output.set('Trimmed PE Reverse Output Filename')
		self.label_reverse_out = Label(self.frame, text="OPTIONAL FOR: If you have separate files for forward and reverse reads, input reverse Output Filename", relief=FLAT, bg="white")
		self.label_reverse_out.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1
		self.reverse_out.grid_remove()# only added when PE is checked
		self.label_reverse_out.grid_remove()

		##If PE, Trimmed Singles Filename
		self.var_singles = StringVar()
		self.singles_out = Entry(self.frame, textvariable = self.var_singles, width=29)
		self.singles_out.grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_singles.set('Trimmed Singles Filename')
		self.label_singles = Label(self.frame, text="OPTIONAL: Trimmed Singles file output will default to TRIMMED_SINGLES.fastq", relief=FLAT, bg="white")
		self.label_singles.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1
		self.singles_out.grid_remove()# only added when PE is checked
		self.label_singles.grid_remove()

		##Quality Value Threshold option
		self.var_q_num = StringVar()
		self.q_num_entry = Entry(self.frame, textvariable = self.var_q_num, width=29)
		self.q_num_entry.grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_q_num.set('Quality Threshold: Input Integer')
		self.q_num_entry_lab = Label(self.frame, text="OPTIONAL: Threshold for trimming based on average quality in a window. Default = 20.", relief=FLAT, bg="white")
		self.q_num_entry_lab.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Length Threshold option
		self.var_L_num = StringVar()
		self.L_num_entry = Entry(self.frame, textvariable = self.var_L_num, width=29)
		self.L_num_entry.grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_L_num.set('Length Threshold: Input Integer')
		self.L_num_entry_lab = Label(self.frame, text="OPTIONAL: Threshold to keep a read based on length after trimming. Default = 20.", relief=FLAT, bg="white")
		self.L_num_entry_lab.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Truncation Value option
		self.var_n = IntVar()
		self.n_button = Checkbutton(self.frame, text="-n", variable = self.var_n, bg="white")
		self.n_button.grid(row = x, column = 0, padx = 5, pady = 5)
		self.n_button_lab = Label(self.frame, text="OPTIONAL: Truncate sequences at position of first N.", relief=FLAT, bg="white")
		self.n_button_lab.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Single Output File for Interleaved Reads
		self.var_m = IntVar()
		self.m_button = Checkbutton(self.frame, text="-M", variable=self.var_m, bg="white")
		self.m_button.grid(row = x, column = 0, padx = 5, pady = 5)
		self.label_m = Label(self.frame, text="OPTIONAL: If you have one file with interleaved reads and you want ONLY one interleaved file as output", relief=FLAT, bg="white")
		self.label_m.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1
		self.m_button.grid_remove()# only added when PE is checked
		self.label_m.grid_remove()

		##No Five Prime Trimming option
		self.var_x = IntVar()
		self.x_button = Checkbutton(self.frame, text="-x", variable=self.var_x, bg="white")
		self.x_button.grid(row = x, column = 0, padx = 5, pady = 5)
		self.x_button_lab = Label(self.frame, text="OPTIONAL: Don't do five prime trimming.", relief=FLAT, bg="white")
		self.x_button_lab.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##G-Zip option
		self.var_g = IntVar()
		self.g_button = Checkbutton(self.frame, text="-g", variable=self.var_g, bg="white")
		self.g_button.grid(row = x, column = 0, padx = 5, pady = 5)
		self.g_button_lab = Label(self.frame, text="OPTIONAL: Output gzipped files.", relief=FLAT, bg="white")
		self.g_button_lab.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1	
		
		self.OPTIONS(x)

		##Error Output To Screen Label
		self.err = StringVar()
		self.err_message = Message(self.frame, text=self.err.get(), aspect = 1000, bg="white")
		self.err_message.grid(row=x,column=0, columnspan=5, padx = 5, sticky = "we")
		return

	def OPTIONS(self, x):

		##When creating the display it will remove all options from the screen initially, however when an option
		##is picked to change, it will display those specific options to change
		
		self.out_file.grid_remove(); self.reverse_out.grid_remove(); self.label_reverse_out.grid_remove(); self.singles_out.grid_remove(); self.label_singles.grid_remove(); self.q_num_entry.grid_remove(); self.L_num_entry.grid_remove(); self.n_button.grid_remove()
		self.m_button.grid_remove(); self.label_m.grid_remove(); self.x_button.grid_remove(); self.g_button.grid_remove(); self.out_file_lab.grid_remove(); self.q_num_entry_lab.grid_remove(); self.L_num_entry_lab.grid_remove(); self.n_button_lab.grid_remove()
		self.x_button_lab.grid_remove(); self.label_L.grid_remove(),self.g_button_lab.grid_remove()

		if(self.var_options.get() == "Display"):
			self.out_file.grid(); self.reverse_out.grid(); self.label_reverse_out.grid(); self.singles_out.grid(); self.label_singles.grid(); self.q_num_entry.grid(); self.L_num_entry.grid(); self.n_button.grid()
			self.m_button.grid(); self.label_m.grid(); self.x_button.grid(); self.g_button.grid(); self.out_file_lab.grid(); self.q_num_entry_lab.grid(); self.L_num_entry_lab.grid(); self.n_button_lab.grid()
			self.x_button_lab.grid(); self.label_L.grid(),self.g_button_lab.grid()

		return

	def Check_Options(self):
		
		##Looks at the options that have been checked off and creates a string##
		##Set the start of the string
		functions.globstring = "./Sickle/sickle-master/sickle"
		##Set errors to nothing
		##If errors present add on string of errors
		errors = ''
		
		##Runs through all the options and creates string for the options that have been marked by the user##
		##If mandatory options not checked or wrong input to an option then add to errors##

		##If Paired-end file
		if(self.var_se_pe.get() == "Paired-end"):
			functions.args_se_pe(self.var_se_pe.get())
			if(self.var_g.get()):
				functions.args_se_and_pe_non_man("-g", "")
			
			if(self.var_reverse_file == ''):
				
				if((".fastq" not in self.var_filename and ".fq" not in self.var_filename) or self.var_filename == ''):
					errors += "Enter file with .fastq or .fq appended to the end\n"
				else:
					functions.file_input_inter(self.var_filename)
				
				if(self.var_qual.get() != "Pick Quality Type"):
					functions.quality_vals(self.var_qual.get())
				else:
					errors += "Enter quality type\n"
				
				if(self.var_m.get()):
					##If Only Want One Output File
					if(self.var_g.get()):
						if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
							functions.inter_big_m('TRIMMED_OUTPUT.fastq.gz')
						elif(".fastq" not in self.var_out_file.get() and ".fq" not in self.var_out_file.get()):
							errors += "Enter file with .fastq or .fq appended to the end\n"
						else:
							functions.inter_big_m(self.var_out_file.get() + '.gz')
					else:
						if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
							functions.inter_big_m('TRIMMED_OUTPUT.fastq')
						elif(".fastq" not in self.var_out_file.get() and ".fq" not in self.var_out_file.get()):
							errors += "Enter file with .fastq or .fq appended to the end\n"
						else:
							functions.inter_big_m(self.var_out_file.get())
				
				else:
					##If Want Trimmed Singles File Too
					if(self.var_g.get()):
						if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
							functions.inter_m('TRIMMED_OUTPUT.fastq.gz')
						elif(".fastq" not in self.var_out_file.get() and ".fq" not in self.var_out_file.get()):
							errors += "Enter file with .fastq or .fq appended to the end\n"
						else:
							functions.inter_m(self.var_out_file.get() + '.gz')
					
						if(self.var_singles.get() == '' or self.var_singles.get() == 'Trimmed Singles Filename'):
							functions.trimmed('TRIMMED_SINGLES.fastq.gz')
						elif(".fastq" not in self.var_singles.get() and ".fq" not in self.var_singles.get()):
							errors += "Enter file with .fastq or .fq appended to the end\n"
						else:
							functions.trimmed(self.var_singles.get() + '.gz')
					else:
						if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
							functions.inter_m('TRIMMED_OUTPUT.fastq')
						elif(".fastq" not in self.var_out_file.get() and ".fq" not in self.var_out_file.get()):
							errors += "Enter file with .fastq or .fq appended to the end\n"
						else:
							functions.inter_m(self.var_out_file.get())
					
						if(self.var_singles.get() == '' or self.var_singles.get() == 'Trimmed Singles Filename'):
							functions.trimmed('TRIMMED_SINGLES.fastq')
						elif(".fastq" not in self.var_singles.get() and ".fq" not in self.var_singles.get()):
							errors += "Enter file with .fastq or .fq appended to the end\n"
						else:
							functions.trimmed(self.var_singles.get())
			
			else:
				##Forward and Reverse Files have Been Inputted
				if((".fastq" not in self.var_filename and ".fq" not in self.var_filename) or (self.var_filename == '')):
					errors += "Enter file with .fastq or .fq appended to the end\n"
				else:
					functions.file_input(self.var_filename)
				
				if(".fastq" not in self.var_reverse_file and ".fq" not in self.var_reverse_file):
					errors += "Enter file with .fastq or .fq appended to the end or clear contents of reverse entry\n"
				else:
					functions.file_rev_input(self.var_reverse_file)
				
				if(self.var_qual.get() != "Pick Quality Type"):
					functions.quality_vals(self.var_qual.get())
				else:
					errors += "Enter quality value\n"
				
				if(self.var_g.get()):
					if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
						functions.output('TRIMMED_OUTPUT.fastq.gz')
					elif('.fastq' not in self.var_out_file.get() and ".fq" not in self.var_out_file.get()):
						errors += "Enter file with .fastq or .fq appended to the end\n"
					else:
						functions.output(self.var_out_file.get() + '.gz')
				else:
					if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
						functions.output('TRIMMED_OUTPUT.fastq')
					elif('.fastq' not in self.var_out_file.get() and ".fq" not in self.var_out_file.get()):
						errors += "Enter file with .fastq or .fq appended to the end\n"
					else:
						functions.output(self.var_out_file.get())
				
				if(self.var_g.get()):
					if(self.var_reverse_output.get() == '' or self.var_reverse_output.get() == 'Trimmed PE Reverse Output Filename'):
						functions.output_rev('TRIMMED_OUTPUT_REV.fastq.gz')
					elif(".fastq" not in self.var_reverse_output.get() and ".fq" not in self.var_reverse_output.get()):
						errors += "Enter file with .fastq or .fq appended to the end\n"
					else:
						functions.output_rev(self.var_reverse_output.get() + '.gz')
				else:
					if(self.var_reverse_output.get() == '' or self.var_reverse_output.get() == 'Trimmed PE Reverse Output Filename'):
						functions.output_rev('TRIMMED_OUTPUT_REV.fastq')
					elif(".fastq" not in self.var_reverse_output.get() and ".fq" not in self.var_reverse_output.get()):
						errors += "Enter file with .fastq or .fq appended to the end\n"
					else:
						functions.output_rev(self.var_reverse_output.get())
				
				if(self.var_g.get()):
					if(self.var_singles.get() == '' or self.var_singles.get() == 'Trimmed Singles Filename'):
						functions.trimmed('TRIMMED_SINGLES.fastq.gz')
					elif(".fastq" not in self.var_singles.get() and ".fq" not in self.var_singles.get()):
						errors += "Enter file with .fastq or .fq appended to the end\n"
					else:
						functions.trimmed(self.var_singles.get() + '.gz')
				else:
					if(self.var_singles.get() == '' or self.var_singles.get() == 'Trimmed Singles Filename'):
						functions.trimmed('TRIMMED_SINGLES.fastq')
					elif(".fastq" not in self.var_singles.get() and ".fq" not in self.var_singles.get()):
						errors += "Enter file with .fastq or .fq appended to the end\n"
					else:
						functions.trimmed(self.var_singles.get())

		##If it's a Single-End File
		elif(self.var_se_pe.get() == "Single-end            "):
			functions.args_se_pe(self.var_se_pe.get())

			if((".fastq" not in self.var_filename and ".fq" not in self.var_filename) or (self.var_filename == '')):
				errors += "Pick file with .fastq or .fq appended to the end\n"
			else:
				functions.file_input(self.var_filename)
			
			if(self.var_qual.get() != "Pick Quality Type"):
				functions.quality_vals(self.var_qual.get())
			else:
				errors += "Enter quality value\n"
			
			if(self.var_g.get()):
				if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
					functions.output('TRIMMED_OUTPUT.fastq.gz')
				elif(".fastq" not in self.var_out_file.get() or ".fq" not in self.var_out_file.get()):
					errors += "Enter file with .fastq or .fq appended to the end\n"
				else:
					functions.output(self.var_out_file.get() + '.gz')

			else:
				if(self.var_out_file.get() == '' or self.var_out_file.get() == 'Output Filename'):
					functions.output('TRIMMED_OUTPUT.fastq')
				elif(".fastq" not in self.var_out_file.get() or ".fq" not in self.var_out_file.get()):
					errors += "Enter file with .fastq or .fq appended to the end\n"
				else:
					functions.output(self.var_out_file.get())
		
		##If SE or PE not Inputted
		else:
			errors += "Enter SE or PE\n"
		
		if(functions.is_int(self.var_q_num.get())):
			functions.args_se_and_pe_non_man("-q", int(self.var_q_num.get()))
		
		if(functions.is_int(self.var_L_num.get())):
			functions.args_se_and_pe_non_man("-l", int(self.var_L_num.get()))
		
		if(self.var_x.get()):
			functions.args_se_and_pe_non_man("-x", "")
		
		if(self.var_n.get()):
			functions.args_se_and_pe_non_man("-n", "")

		
		##If there are no errors than run the string with Sickle
		##If you need to compile the file it compiles it for you as long as makefile is there
		##Put the Output to the Screen from the program run
		##If there are errors put them to the screen
		self.err_message.config(text="Running....", font="Times 18")
		self.update()
		if(errors == ''):
			cmd_line = shlex.split(functions.globstring)
			if('sickle' in os.listdir('./Sickle/sickle-master/')):
				subprocess.call(['chmod', '+x', './Sickle/sickle-master/sickle'])
				p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				result, error = p.communicate()
				if(error.decode('utf-8') == ''):
					self.err_message.config(text="OUTPUT: \n" + result.decode('utf-8'), font="Times 18")
				else:
					self.err_message.config(text='\nERRORS: \n' + error.decode('utf-8'), font="Times 18")
			elif('sickle' not in os.listdir('./Sickle/sickle-master/') and 'Makefile' in os.listdir('./Sickle/sickle-master/')):
				subprocess.call(["make", "-C", "./Sickle/sickle-master/"])
				p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				result, error = p.communicate()
				if(error.decode('utf-8') == ''):
					self.err_message.config(text="OUTPUT: \n" + result.decode('utf-8'), font="Times 18")
				else:
					self.err_message.config(text='\nERRORS: \n' + error.decode('utf-8'), font="Times 18", fg='dark red')
			else:
				self.err_message.config(text="ERRORS: \n makefile not in correct directory", fg='dark red', font="Times 18")
		else:
			self.err_message.config(text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")
		
		return

	def SE_and_PE(self, another):#
		##Function that adds to Input File Options if PE is Picked
		
		if(self.var_se_pe.get() == "Paired-end" and self.var_options.get() == "Display"):
			self.browse_file2.grid()
			self.label_reverse.grid()
			self.reverse_out.grid()
			self.label_reverse_out.grid()
			self.label_filename.config(text="MANDATORY: If you have one file with interleaved forward and reverse reads enter filename, otherwise enter paired-end forward fastq file")
			self.singles_out.grid()
			self.label_singles.grid()
			self.m_button.grid()
			self.label_m.grid()

		if(self.var_se_pe.get() == "Paired-end" and self.var_options.get() != "Display"):
			self.browse_file2.grid()
			self.label_reverse.grid()
			self.label_filename.config(text="MANDATORY: If you have one file with interleaved forward and reverse reads enter filename, otherwise enter paired-end forward fastq file")

		elif(self.var_se_pe.get() == "Single-end            "):
			self.browse_file2.grid_remove()
			self.label_reverse.grid_remove()
			self.reverse_out.grid_remove()
			self.label_reverse_out.grid_remove()
			self.label_filename.config(text="MANDATORY: Input File: Input filename with .fastq at end")
			self.singles_out.grid_remove()
			self.label_singles.grid_remove()
			self.m_button.grid_remove()
			self.label_m.grid_remove()

		return

	
	##Gives ability to Browse for a file and sets to a variable
	def browse_file_input1(self):
		self.var_filename = filedialog.askopenfilename()
		return

	##Gives ability to Browse for a file and sets to a variable
	def browse_file_input2(self):
		self.var_reverse_file = filedialog.askopenfilename()
		return

	def onFrameConfigure(self, event):
		#Reset the scroll region to encompass the inner frame
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		return


if __name__ == "__main__":
	##Start of App
	##Creates Window and goes to the Mainloop of the class and creates the App
	root=Tk()
	root.wm_title("SICKLE")
	root.geometry('975x575')
	App(root).pack(side="top", fill="both", expand=True)
	root.mainloop()

#add comments
