
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
# args_se_and_pe_non_man - Determines which string to add to globstring based
# on arguments given
#
# inter_m - Adds -m and argument to globstring based on interleaved file
#
# inter_big_m - Adds -M and argument to globstring based on interleaved file
#
# file_input_inter - Adds -c and argument to globstring based on interleaved
# file given
#
# trimmed - Adds -s and argument to globstring based on trim argument given
#
# file_input - Adds -f and argument to globstring based on input file given
#
# file_rev_input - Adds -r and argument to globstring based on reverse
# file given
#
# quality_vals - Adds quality type inputted to globstring
#
# output_rev - Adds -p and argument to globstring based on output reverse
# file given
#
# output - Adds -o and argument to globstring based on output file given
#
# args_se_pe - Adds file type to globstring
#
##############################################################################

globstring = "./GenCoF-master/Sickle/sickle-master/sickle"

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def args_se_and_pe_non_man(arg1, arg2):
    global globstring
    if (arg1 == '-q' and isinstance(arg2, int)):
        globstring += " -q "
        arg2 = str(arg2)
        globstring += arg2
    elif (arg1 == '-l' and isinstance(arg2, int)):
        globstring += " -l "
        arg2 = str(arg2)
        globstring += arg2
    elif (arg1 == '-x'):
        globstring += " -x "
    elif (arg1 == '-n'):
        globstring += " -n "
    elif (arg1 == '-g'):
        globstring += " -g"
    return

def inter_m(arg1):
    global globstring
    globstring += ' -m '
    globstring += arg1
    return

def inter_big_m(arg1):
    global globstring
    globstring += ' -M '
    globstring += arg1
    return

def file_input_inter(arg1):
    global globstring
    globstring += ' -c '
    globstring += arg1
    return

def trimmed(arg1):
    global globstring
    globstring += ' -s '
    globstring += arg1
    return

def file_input(arg1):
    global globstring
    globstring += " -f '"
    globstring += arg1 + "'"
    return

def file_rev_input(arg1):
    global globstring
    globstring += " -r '"
    globstring += arg1 + "'"
    return

def quality_vals(arg1):
    global globstring
    globstring += ' -t '
    if (arg1 == 'Solexa                '):
        globstring += 'solexa'
    elif (arg1 == 'Illumina'):
        globstring += 'illumina'
    elif (arg1 == 'Sanger'):
        globstring += 'sanger'
    return

def output_rev(arg1):
    global globstring
    globstring += ' -p ./'
    globstring += arg1
    return

def output(arg1):
    global globstring
    globstring += ' -o ./'
    globstring += arg1
    return

def args_se_pe(arg1):
    global globstring
    if (arg1 == 'Single-end            '):
        globstring += ' se'
    elif (arg1 == 'Paired-end'):
        globstring += ' pe'
    return
