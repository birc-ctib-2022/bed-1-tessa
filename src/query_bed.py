"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from bed import (
    BedLine, parse_line, print_line
)
from query import Table


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    # FIXME: put your code here

    table = Table()

    for line in args.bed: 
        variable = parse_line(line)
        table.add_line = print_line(variable)
    
    for index_args in args.query: 
    #for every line in input query 
        query_setup = line.split("\t")
        #make a new variable called query_setup 
        # hat is each line with each item tab seperated 
        query_chromosome = query_setup [0]
        #make a new variable called query_chrom 
        #that is the 0 index which we know is the name of the 
        #chromosome 
        query_chromosome_start = int(query_setup [1])
        #make a new variable called query_chrom_start
        #that is an integer that is the start of the feature 
        query_chromosome_end = int(query_setup [2])
        #make a new variable called query_chrom_end
        #that is an integer that is the end of the feature 

        chromosome_list= table.get_chrom(query_chrom) 
        # REMINDER from query.py this was set up: 
        #  def get_chrom(self, chrom: str) -> list[BedLine]:
        #"""Get all the lines that sits on chrom"""
        # return self.tbl[chrom]
       
        for index_chromosome_list in chromosome_list: 
            bed_chromosome = variable[0]
            bed_chromosome_start = int(variable [1])
            bed_chromosome_end = int(variable [2])

            if query_chromosome_start <= bed_chromosome_start and query_chromosome_end>= bed_chromosome_end:
                print_line(index_chromosome_list,args.outfile)


 

if __name__ == '__main__':
    main()
