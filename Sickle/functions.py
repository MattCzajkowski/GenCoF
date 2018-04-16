##Functions for Check Options in sickle-gui.py

globstring = "./sickle-master/sickle"

#checks if value is an integer
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

##Rest of functions add string options to global variable globstring

def args_se_and_pe_non_man(arg1, arg2):
    global globstring
    if(arg1 == '-q' and isinstance(arg2, int)):
        globstring += " -q "
        arg2 = str(arg2)
        globstring += arg2
    elif(arg1 == '-l' and isinstance(arg2, int)):
        globstring += " -l "
        arg2 = str(arg2)
        globstring += arg2
    elif(arg1 == '-x'):
        globstring += " -x "
    elif(arg1 == '-n'):
        globstring += " -n "
    elif(arg1 == '-g'):
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
    if(arg1 == 'Solexa                '):
        globstring += 'solexa'
    elif(arg1 == 'Illumina'):
        globstring += 'illumina'
    elif(arg1 == 'Sanger'):
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
    if(arg1 == 'Single-end            '):
        globstring += ' se'
    elif(arg1 == 'Paired-end'):
        globstring += ' pe'
    return
