import shlex, subprocess, os, sys
from tkinter import filedialog
from tkinter import *

#Specifications: Requires cat executable, Python 3 module Tkinter, and Linux environment
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
		self.file1_title = Label(self.frame, text="Join", font="Times 20 bold", bg="white").grid(row = x, column = 0, columnspan = 10, padx = 5, pady = (5,5), sticky = "we")
		x += 1

		##Input File Section
		self.var_filename = ''
		self.browse_file = Button(self.frame, text="Browse", command=self.browse_file_input1, width=15)
		self.browse_file.grid(row = x, column = 0, padx = 5, pady = 5)
		self.label_filename = Label(self.frame, text="Input Files: Pick input files. Use control or shift click to select multiple files at a time", relief=FLAT, bg="white")
		self.label_filename.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Input File Type Section
		self.var_file_type = StringVar()
		self.var_file_type.set("Pick File Type")
		self.file_type = OptionMenu(self.frame, self.var_file_type, "FASTA", "FASTQ").grid(row = x, column = 0, padx = 5, pady = 5)
		Label(self.frame, text="MANDATORY: File type as input ", relief=FLAT, bg="white").grid(row = x, column = 1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Output Filename Section
		self.var_out_file = StringVar()
		self.out_file = Entry(self.frame, textvariable = self.var_out_file, width=29).grid(row = x, column = 0, padx = 5, pady = 5)
		self.var_out_file.set('Output Filename')
		Label(self.frame, text="Output File: Will default to JOINED_OUTPUT with file type appended to end", relief=FLAT, bg="white").grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Run Button which goes to function: Check_Options when clicked
		self.run_button = Button(self.frame, text="Run Join", command=self.Check_Options)
		self.run_button.grid(row=x,column=1, padx = 5, pady = 5, sticky = "w")
		x += 1

		##Error Output To Screen Label
		self.err = StringVar()
		self.err_message = Label(self.frame, text=self.err.get(), relief=FLAT, justify=LEFT, bg="white")
		self.err_message.grid(row=x,column=0, columnspan=5, padx = 5, sticky = "w")

		return

	def Check_Options(self):

		if (sys.platform == 'win32'):
			globstring = 'type '
		else:
			globstring = 'cat '
		##Looks at the options that have been checked off and creates a string##
		##Set the start of the string

		##Set errors to nothing
		##If errors present add on string of errors
		errors = ''

		##Runs through all the options and creates string for the options that have been marked by the user##
		##If mandatory options not checked or wrong input to an option then add to errors##

		if(self.var_filename == ''):# Get Input Filename
			errors += "Enter Input Files\n"
		else:
			globstring += "'" + "' '".join(self.var_filename) + "'" + " "


		globstring += "> "

		if(self.var_out_file.get() == "Output Filename" or self.var_out_file.get() == ""):
			globstring += "JOINED_OUTPUT"
		else:
			globstring += self.var_out_file.get()

		if(self.var_file_type.get() == "Pick File Type"):
			errors += "Enter Input File type\n"
		elif(self.var_file_type.get() == "FASTA"):
			globstring += ".fasta"
		else:
			globstring += ".fastq"

		##If there are no errors than run the string with Join
		##Put the Output to the Screen from the program run
		##If there are errors put them to the screen
		self.err_message.config(text="Running....", font="Times 18")
		self.update()
		if(errors == ''):
			cmd_line = shlex.split(globstring)
			##Actually run process
			p = subprocess.Popen(globstring, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			output, error = p.communicate()
			if(error.decode('utf-8') == ''):
				self.err_message.config(text="OUTPUT: \n" + output.decode('utf-8') + "Completed", font="Times 18")
			else:
				self.err_message.config(text='\n' + error.decode('utf-8'), font="Times 18", fg='dark red')
		else:
			self.err_message.config(text=('ERRORS: \n' + errors), fg='dark red', font="Times 18")
		return
	
	def browse_file_input1(self):
		self.var_filename = filedialog.askopenfilenames(title='Choose a file')
		print(self.var_filename + "\n")
		self.var_filename = self.var_filename.split(os.sep)
		print(self.var_filename + "\n")
		self.var_filename = os.path.join(*self.var_filename)
		print(self.var_filename + "\n")
		return
	
	def onFrameConfigure(self, event):
		#Reset the scroll region to encompass the inner frame
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))


		return

if __name__ == "__main__":
	##Start of App
	##Creates Window and goes to the Mainloop of the class and creates the App
	root=Tk()
	root.wm_title("Join")
	root.geometry('900x300')
	App(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
