##############################################################################
#
# is_int - Checks if argument is an integer
#
##############################################################################

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
