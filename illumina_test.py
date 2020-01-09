from pathlib import Path
from pathlib import PurePath
import os
import subprocess
import logging
import argparse
import shutil


p = Path.cwd()
new_dir = Path(p.parents[0]).joinpath("test")
Path.mkdir(new_dir)
discovered_fastqs = []
list_of_fastq = list(p.glob('**/*'))

for item in list_of_fastq:
    filename = item.name
    filesize = item.stat().st_size
    discovered_fastqs.append(tuple([tuple([filename, filesize]), item]))
'''
duplicates = []
final_list = []
for item in discovered_fastqs:

    filename = item[0][0]
    if filename not in final_list:
        final_list.append(filename)
    else:
        duplicates.append(filename)

item_to_remove = []
# looks over items that were duplicated and finds the object associated with the filename and creates a list of objects
for item in duplicates:
    for source in discovered_fastqs:
        if item == source[0][0]:
            item_to_remove.append(source)
# sorts list of objects based on filesize
sorted(item_to_remove, key=lambda x: x[0][1])
# removes objects from filelist until no more duplicates remain, will be removing the small files first
while duplicates != []:
    #print(duplicates)
    for thing in item_to_remove:
        discovered_fastqs.remove(thing)
        duplicates.remove(thing[0][0])
print(str(discovered_fastqs))
'''