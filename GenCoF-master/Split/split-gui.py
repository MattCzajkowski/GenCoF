import shlex, subprocess, os, sys
from tkinter import filedialog
from tkinter import *

#Specifications: Requires Perl and Python 3 module Tkinter

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
		self.file1_title = Label(self.frame, text="Split", font="Times 24 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = (5,5), sticky = "we")
		x += 1

		##Title for Mandatory Section
		self.fill_mandat = Label(self.frame, text="""Citation: Kryukov K. (2012-2017).FASTA SPLITTER: Splits Fasta Files into parts. Available online at: http://kirill-kryukov.com/study/tools/fasta-splitter/
 Kryukov K. (2012-2017).FASTQ SPLITTER: Splits Fastq Files into parts. Available online at: http://kirill-kryukov.com/study/tools/fastq-splitter/""", font="Times 11 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = 5, sticky = "we")
		x += 1

		##Title for Mandatory Section
		self.fill_mandat = Label(self.frame, text="***Must fill all MANDATORY sections***", relief=FLAT, font="Times 16 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = 5, sticky = "we")
		x += 1

		##Input File Section
		self.var_filename = ''
		self.browse_file = Button(self.frame, text="Browse", command=self.browse_file_input1, width=15)
		self.browse_file.grid(row = x, column = 0, padx = 5, pady = 5)
		self.label_filename = Label(self.frame, text="MANDATORY: Input File: Input file that is in fastq or fasta format", relief=FLAT, bg="white")
		self.label_filename.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Input File Type Section
		self.var_file_type = StringVar()
		self.var_file_type.set("Pick File Type")
		self.file_type = OptionMenu(self.frame, self.var_file_type, "FASTA", "FASTQ").grid(row = x, column = 0, padx = 5, pady = 5)
		Label(self.frame, text="MANDATORY: File type as input ", relief=FLAT, bg="white").grid(row = x, column = 1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Input Amount of Files to Split Into
		self.var_n_parts = StringVar()
		self.n_parts = Entry(self.frame, textvariable = self.var_n_parts, width=28)
		self.n_parts.grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_n_parts.set('Divide File Parts')
		Label(self.frame, text="""Input integer for amount of files you want your input file to be broken up into""", relief=FLAT, justify=LEFT, bg="white").grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Run Button which goes to function: Check_Options when clicked
		self.run_button = Button(self.frame, text="Run Split", command=self.Check_Options)
		self.run_button.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Error Output To Screen Label
		self.err = StringVar()
		self.err_message = Label(self.frame, text=self.err.get(), relief=FLAT, justify=LEFT, bg="white")
		self.err_message.grid(row=x,column=0, columnspan=5, padx = 5, sticky = "w")

		return

	def Check_Options(self):

		globstring = ''
		##Looks at the options that have been checked off and creates a string##
		##Set the start of the string

		##Set errors to nothing
		##If errors present add on string of errors
		errors = ''

		if(self.var_file_type.get() == "FASTA"):
			globstring = "perl ./GenCoF-master/Split/Split_files/fasta-splitter.pl "
		elif(self.var_file_type.get() == "FASTQ"):
			globstring = "perl ./GenCoF-master/Split/Split_files/fastq-splitter.pl "
		else:
			errors += "No file type picked\n"

		##Runs through all the options and creates string for the options that have been marked by the user##
		##If mandatory options not checked or wrong input to an option then add to errors##

		if(self.var_filename == ''):# Get Input Filename
			errors += "Enter Input File\n"
		else:
			globstring += "'" + self.var_filename + "'" + " "

		if(self.var_n_parts.get() == "Divide File Parts" or self.var_n_parts.get() == ""):
			errors += "Enter Integer for amount of parts for file to broken up into\n"
		else:
			globstring += "--n-parts " + self.var_n_parts.get()

		##If there are no errors than run the string with Deconseq
		##Put the Output to the Screen from the program run
		##If there are errors put them to the screen
		self.err_message.config(text="Running....", font="Times 18")
		self.update()		
		if(errors == ''):
			cmd_line = shlex.split(globstring)
			if('fasta-splitter.pl' in os.listdir('./GenCoF-master/Split/Split_files/') and 'fastq-splitter.pl' in os.listdir('./GenCoF-master/Split/Split_files/')):
				p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				output, error = p.communicate()
				if(error.decode('utf-8') == ''):
					self.err_message.config(text="OUTPUT: \n" + output.decode('utf-8'), font="Times 18")
				else:
					self.err_message.config(text='\nERRORS: \n' + error.decode('utf-8'), font="Times 18", fg='dark red')
			else:
				self.err_message.config(text="ERRORS: \n Fastq or Fasta splitter not in correct directory", fg='dark red', font="Times 18")
		else:
			self.err_message.config(text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")
		return

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
	root=Tk()
	root.wm_title("Split")
	root.geometry('800x350')
	App(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
