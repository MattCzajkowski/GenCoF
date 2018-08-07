
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
##############################################################################

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
