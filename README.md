# GenCoF (An interface for contamination filtering)

GenCoF is a graphical user interface for a genomic contamination filtering pipeline to filter out human reads from metagenomic files through the programs Sickle or Prinseq, Bowtie2, and Fastq or Fasta Splitter.

## Dependancies:
This project requires:
* Mac OS or Linux
* Python 3 with module Tkinter
* GNU like environment with GCC, GNU Make etc.
* Perl Version 5.18 or greater
* Thread Building Blocks which is commonly included with many operating systems. If not installed, download from "https://github.com/01org/tbb/releases" and follow the necessary steps to install or if on Mac OS use "brew install tbb" from command line or follow the steps on the following page "http://tbb.readthedocs.io/en/latest/gettingstarted.html" for Linux.
* Human Genomic Sequences are required as well if you plan on removing human sequences from your reads. This version doesn't include them, however, they can be downloaded from the Bowtie2 NCBI databases which can be found at https://support.illumina.com/sequencing/sequencing_software/igenome.html. Many other common reference genomes can be downloaded from here to decontaminate your sequences. See Usage below for a tutorial.

Citations are provided at the top of each application.

## Setup

### MacOS
Once the file has been downloaded it will appear as a zip file.  You can unpack the folder by right clicking on it and using the archive manager, double clicking the file or using the command:

    unzip GenCoF.zip

from the correct directory in terminal.

To make GenCoF a proper executable within the folder all that needs to be done is to Right Click on the app labeled GenCoF(Mac) and click open. You will then be prompted with ““GenCoF” is from an unidentified developer. Are you sure you want to open it?”.
From there click Open and you may be prompted with a password depending on security preferences.  After that it is ready to use.

See **Common Errors** if you at any point of opening it you are prompted with ""GenCoF(Mac)" is damaged and can't be opened. You should move it to the Trash".

Once this is done, you are free to double click the file labeled GenCoF and begin filtering your samples!!

### Linux
Once the file has been downloaded it will appear as a zip file.  You can unpack the folder by right clicking on it and using the archive manager, double clicking the file and clicking the extract in the upper left corner or using the command:

    unzip GenCoF.zip

from the correct directory in terminal.

To make GenCoF a proper executable within the folder, right click on GenCoF(Linux) and go to properties. Once there click on the tab labeled permissions and check off the box labeled "Allow executing file as program".

Once this is done, you are free to double click the file labeled GenCoF and begin filtering your samples!!


## Usage

Running GenCoF is easy as all descriptions for each program option are labeled right next to the option itself. 
Always run each application by starting at GenCoF and navigating to the appropriate application. If you are running on MacOS, the terminal that opens with the program is necessary as the program uses it to run the applications. If you would like to exit the program at any time such as a running process you can do so by exiting the terminal. README's for each program are located within their respective program folders, however, they do not necessarily correspond well to the graphical user interface.

For large files(> 1GB) it may take significant time to run the Bowtie2 application so it is recommended to either thread the files depending on the amount of cores your computer has or to split the files up and join them back together once Bowtie2 has been run.

To create reference databases from the site https://support.illumina.com/sequencing/sequencing_software/igenome.html click on the build you would like to download from.  Once it is downloaded, open it and unpack it according the file type downloaded (ie. through an archive manager by double clicking on the file or via the command line with 'tar xvf filename.tar', 'unzip filename.zip', 'gunzip filename.gz'...). Once done find the 'Bowtie2Index' folder within the reference folder and move the contents of that folder (the .fa file isn't necessary) to the folder path GenCoF-master/Bowtie2/bowtie2-2.3.4.1 and you are ready to decontaminate your samples through GenCoF. Rename your folder accordingly. If you would like to build your own reference database(in case your genome isn't located on Bowtie2's website), you can use bowtie2-build within GenCoF to build a database.

## Output

Program specific output:
* Sickle and Prinseq: Output a single file of fastq or fasta format (whichever specified).
* Split: Outputs the amount of files specified in the program as input.
* Bowtie2: Outputs two files: one file that contains reads mapped to the reference database and one file that contains reads unmapped to the reference database.
* Join: Outputs a file of joined input files.

The program Split outputs files to where the input file was. All other programs output files to the main folder GenCoF. 

## Common Errors

When the error of ""GenCoF(Mac)" is damaged and can't be opened. You should move it to the Trash" comes up, security preferences need to be changed. You can fix this error by going to the apple in the upper left and selecting "Security Preferences". After that, go to "Security and Privacy" and click the lock in the bottom right. You may be prompted with a password. After that select the button "Allow apps from: unidentified developers" and reclick the lock button. After that just reopen the app by double clicking on GenCoF.

Avoid changing names of files that have been downloaded as this will cause problems for the programs running.
