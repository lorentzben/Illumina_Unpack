# A python script to unpack fastq files from illumina basespace and place in a folder
from pathlib import Path
from pathlib import PurePath
import os
import subprocess
import logging
import argparse
import shutil
import re
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Logging handler which catches EVERYTHING
file_logger = logging.FileHandler('unpack_illumina.log')
file_logger.setLevel(logging.DEBUG)
# Logging handler which logs less
console_logger = logging.StreamHandler()


def set_up_logger(quiet):
    if quiet:
        console_logger.setLevel(logging.WARNING)
    else:
        console_logger.setLevel(logging.INFO)


# Formats the logs so they are pretty
logFormatter = '%(asctime)s- %(name)s - %(lineno)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(logFormatter)
file_logger.setFormatter(formatter)
console_logger.setFormatter(formatter)

# adds handlers to logger
logger.addHandler(file_logger)
logger.addHandler(console_logger)


def create_index_of_fastq(project_name):
    p = Path.cwd()
    new_dir = Path(p.parents[0]).joinpath(project_name)
    try:
        Path.mkdir(new_dir)
    except FileExistsError:
        pass
    discovered_fastqs = []
    list_of_fastq = list(p.glob('**/*.fastq.gz'))
    # getting filename filesize and location for all .fastq files below the current dir
    for item in list_of_fastq:
        filename = item.name
        filesize = item.stat().st_size
        discovered_fastqs.append(tuple([tuple([filename, filesize]), item]))

    logger.info("Created table of filenames, filesizes and path location")
    logger.debug(discovered_fastqs)
    return discovered_fastqs

# checks to see if there are duplicate read names, returns [] if none


def discover_duplicates(list_of_fastqs):
    duplicates = []
    final_list = []
    for item in list_of_fastqs:

        filename = item[0][0]
        if filename not in final_list:
            final_list.append(filename)
        else:
            duplicates.append(filename)
    logger.debug(duplicates)
    return duplicates

# removes duplicate reads names and favors larger filesize returns updated list


def unique_fastq_list(duplicates, discovered_fastqs):

    item_to_remove = []
    # looks over items that were duplicated and finds the object associated with the filename and creates a list of objects
    for item in duplicates:
        for source in discovered_fastqs:
            if item == source[0][0]:
                item_to_remove.append(source)
    # sorts list of objects based on filesize
    sorted(item_to_remove, key=lambda x: x[0][1])
    # removes objects from filelist until no more duplicates remain, will be removing the small files first
    for item in item_to_remove:
        file_size = item[0][1]
        for thing in discovered_fastqs:
            if thing[0][0] == item[0][0]:
                if thing[0][1] < item[0][1]:
                    discovered_fastqs.remove(thing)
    logger.debug(discovered_fastqs)
    return discovered_fastqs


def move_fastq_to_output_dir(discover_fastqs, new_dir):
    for item in discover_fastqs:
        shutil.move(str(item[1]), str(new_dir))
        logger.debug("Moved " + str(item[0][0]))
    logger.info("all files moved")

def rename_fastqs(current_dir,fastqs_to_rename):
    regex = r"-*_*"
    subst = ''
    new_names_for_design = []
    for item in fastqs_to_rename:
        old_name = str(item[0][0])
        new_name = re.sub(regex, subst, old_name, 0)
        #pulls off the .fastq 
        new_name_no_ext = new_name[:-6]
        #this is gonna be written out to file
        new_names_for_design.append(new_name_no_ext)
        os.rename(current_dir.joinpath(Path(old_name)), current_dir.joinpath(Path(new_name)))
    try:
        with open("design_INTERMEDIATE.txt",'r+') as temp_design:
            wr = csv.writer(temp_design, quoting=csv.QUOTE_ALL)
            wr.writerow(new_names_for_design)
        logger.INFO("There is a temp design file that needs catagories added in this dir")
    except 

def unzip_fastqgz(new_dir):
    os.chdir(new_dir)
    logging.info("Please wait while files are unzipped")
    os.system("gunzip *.gz")
    logger.info("All files unzipped")


def main(args):
    p = Path.cwd()
    new_dir = Path(p.parents[0]).joinpath(args.job_name)
    list_of_fastqs = create_index_of_fastq(args.job_name)
    logger.info("number of fastq.gz files found: %s" % len(list_of_fastqs))
    list_of_duplicates = discover_duplicates(list_of_fastqs)
    logger.info("number of duplicate files found: %g" %
                len(list_of_duplicates))
    if list_of_duplicates != []:
        unique_fastq_files = unique_fastq_list(
            list_of_duplicates, list_of_fastqs)
        fastq_to_move = unique_fastq_files
    else:
        fastq_to_move = list_of_fastqs
    move_fastq_to_output_dir(fastq_to_move, new_dir)
    rename_fastqs(new_dir,fastq_to_move)
    if args.unpack:
        unzip_fastqgz(new_dir)
    logger.info("You should be all set")


if __name__ == "__main__":
    # TODO choose extention or have it default to fastq.gz
    # Build Argument Parser in order to facilitate ease of use for user
    parser = argparse.ArgumentParser(
        description="Un-Nests fastq data from illumina")
    parser.add_argument('-n', action='store', required=True,
                        help="name for analysis, will be filename for resultant directory", dest='job_name')

    parser.add_argument('-u', action='store_true', default=False, help='Unpacks the tar archive, requires tar to be installed, suggested', dest='unpack'
                        )
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help="Reduces the amount of text printed to terminal, check logfiles more often", dest='quiet')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')

    args = parser.parse_args()
    main(args)
