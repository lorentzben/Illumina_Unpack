from pathlib import Path
from pathlib import PurePath
import os
import subprocess
import logging
import argparse
import shutil

#first method
p = Path.cwd()
new_dir = Path(p.parents[0]).joinpath("test")
Path.mkdir(new_dir)
discovered_fastqs = []
list_of_fastq = list(p.glob('**/*'))

for item in list_of_fastq:
    filename = item.name
    filesize = item.stat().st_size
    discovered_fastqs.append(tuple([tuple([filename, filesize]), item]))
print(str(discovered_fastqs))
#Second method
duplicates = []
final_list = []
for item in discovered_fastqs:

    filename = item[0][0]
    if filename not in final_list:
        final_list.append(filename)
    else:
        duplicates.append(filename)
print(duplicates)

#third method
item_to_remove = []
# looks over items that were duplicated and finds the object associated with the filename and creates a list of objects
for item in duplicates:
    for source in discovered_fastqs:
        if item == source[0][0]:
            item_to_remove.append(source)
# sorts list of objects based on filesize
sorted(item_to_remove, key=lambda x: x[0][1])

# removes objects from filelist until no more duplicates remain, will be removing the small files first
place_to_delete = []
for i in range(0,len(item_to_remove)):
    for j in range(0,len(discovered_fastqs)):
        if item_to_remove[i] == discovered_fastqs[j]:
            place_to_delete.append(j)
print(place_to_delete)
for place in place_to_delete:
    del discovered_fastqs[place]
print(str(discovered_fastqs))
