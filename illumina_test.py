from pathlib import Path
from pathlib import PurePath
import os
import subprocess
import logging
import argparse
import shutil


p = Path.cwd()
new_dir = Path(p.parents[0]).joinpath(project_name)
Path.mkdir(new_dir)
discovered_fastqs = []
list_of_fastq = list(p.glob('**/*.fastq.gz'))

for item in list_of_fastq:
    filename = item.name
    filesize = item.stat().st_size
    discovered_fastqs.append(tuple([tuple([filename, filesize]), item]))

duplicates = [] 
for item in discovered_fastqs:
        
    filename = item[0][0]
    if filename not in final_list:
        final_list.append(filename)
    else:
        duplicates.append(filename)

item_to_remove = []
#looks over items that were duplicated and finds the object associated with the filename and creates a list of objects
for item in duplicates:
    for source in discovered_fastqs:
        if item == source[0][0]:
            item_to_remove.append(source)
#sorts list of objects based on filesize
sorted(item_to_remove, key=lambda x:x[0][1])
#removes objects from filelist until no more duplicates remain, will be removing the small files first
while list_of_duplicates is not []:
    for thing in item_to_remove:
        discovered_fastqs.remove(thing)
        duplicates.remove(thing[0][0])
print(str(list_of_fastqs))
    
