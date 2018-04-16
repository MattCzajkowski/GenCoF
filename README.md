# GenCoF (An interface for contamination filtering)
### Author: Matthew Czajkowski

GenCoF is a graphical user interface for a genomic contamination filtering pipeline to filter out human reads from metagenomic files through the programs Sickle or Prinseq, Bowtie2, and Fastq or Fasta Splitter.

## Dependancies:
This project requires:
* Mac OS or Linux
* Python 3 with module Tkinter
* GNU like environment with GCC, GNU Make etc.
* Perl Version 5.18 or greater
* Human Genomic Sequences are required as well if you plan on removing human sequences from your reads. This version doesn't include them however they can be downloaded from the Bowtie2 NCBI databases which can be found at https://support.illumina.com/sequencing/sequencing_software/igenome.html. Many other common reference genomes can be downloaded from here to decontaminate your sequences.  Once downloaded just put them in the Bowtie2/bowtie2-2.3.4.1 folder and you are ready to decontaminate your samples through GenCoF.

Citations are provided at the top of each application.

## Setup

# MacOS
Once the file has been downloaded it will appear as a zip file.  You can unpack the folder by right clicking on it and using the archive manager, double clicking the file or using the command:

    unzip GenCoF.zip

from the correct directory in terminal.

To make GenCoF a proper executable within the folder all that needs to be done is to Right Click on the app labeled GenCoF(Mac) and click open and you will be prompted with ““GenCoF” is from an unidentified developer. Are you sure you want to open it?”.
From there click Open and you may be prompted with a password depending on security preferences.  After that it is ready to use.

See **Common Errors** if you at any point of opening it you are prompted with ""GenCoF(Mac)" is damaged and can't be opened. You should move it to the Trash".

Once this is done, you are free to double click the file labeled GenCoF and begin filtering your samples!!

# Linux
Once the file has been downloaded it will appear as a zip file.  You can unpack the folder by right clicking on it and using the archive manager, double clicking the file and clicking the extract in the upper left corner or using the command:

    unzip GenCoF.zip

from the correct directory in terminal.

To make GenCoF a proper executable within the folder, right click on GenCoF(Linux) and go to properties. Once there click on the tab labeled permissions and check off the box labeled "Allow executing file as program".

Once this is done, you are free to double click the file labeled GenCoF and begin filtering your samples!!


## Usage

Running GenCoF is easy as all descriptions for each program option are labeled right next to the option itself. 
Always run each application by starting at GenCoF and navigating to the appropriate application. If you are running on MacOS, the terminal that opens with the program is necessary as the program uses it to run the applications. If you would like to exit the program at any time you can do so by exiting the terminal. README's for each program are located within their respective program folders however they do not necessarily correspond well to the graphical user interface.

For large files(> 1GB) it may take significant time to run the Bowtie2 application so it is recommended to either thread the files depending on the amount of cores your computer has or to split the files up and join them back together once Bowtie2 has been run.

## Output

Program specific output:
* Sickle and Prinseq: Output a single file of fastq or fasta format (whichever specified).
* Split: Outputs the amount of files specified in the program as input.
* Bowtie2: Outputs a file that contains reads mapped to the reference and a file that contains reads unmapped to the reference database.
* Join: Outputs a file of joined input files.

The program Split outputs files to where the input file was. All other programs output files to the main folder GenCoF. 

## Common Errors

When the error of ""GenCoF(Mac)" is damaged and can't be opened. You should move it to the Trash" comes up, security preferences need to be changed. You can fix this error by going to the apple in the upper left and selecting "Security Preferences". After that, go to "Security and Privacy" and click the lock in the bottom right. You may be prompted with a password. After that select the button "Allow apps from: unidentified developers" and reclick the lock button. After that just reopen the app by double clicking on GenCoF.

Avoid changing names of files that have been downloaded as this will cause problems for the programs running.
