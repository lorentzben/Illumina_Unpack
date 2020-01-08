# A python script to unpack fastq files from illumina basespace and place in a folder
from pathlib import Path
from pathlib import PurePath
import os
import subprocess
import logging
import argparse
import shutil


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Logging handler which catches EVERYTHING
file_logger = logging.FileHandler('fastq_for_me.log')
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
    Path.mkdir(new_dir)
    discovered_fastqs = []
    list_of_fastq = list(p.glob('/*.fastq.gz'))

    for item in list_of_fastq:
        filename = item.name()
        filesize = item.stat().st_size
        discovered_fastqs.append(((filename, filesize), item))

    logging.info("Created table of filenames, filesizes and path location")


def move_fastq_to_output_dir(index):
    print("moved")


def unzip_fastqgz():
    print("unzipped")


def main(args):
    logging.critical(
        "Need to make dir and then copy the files located into the dir")
    set_up_logger(args.quiet)

    index = create_index_of_fastq()
    move_fastq_to_output_dir(index)
    unzip_fastqgz()


if __name__ == "__main__":
    # Build Argument Parser in order to facilitate ease of use for user
    parser = argparse.ArgumentParser(
        description="Perform Automated Analysis and Formatting of Sequence Data")
    parser.add_argument('-s', '--silent', action='store_true', default=False,
                        help='does not create a human readable copy of the table only writes to file', dest='silent')
    parser.add_argument('-f', '--no-file', action='store_true', default=False,
                        help='does not create a computer readable file must use -r flag for human readability', dest='comp')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help="Reduces the amount of text printed to terminal, check logfiles more often", dest='quiet')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')

    args = parser.parse_args()
    main(args)
