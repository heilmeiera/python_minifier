import glob
import os
import re
from shutil import copyfile, rmtree

"""
Created by:
Alexander Heilmeier

Documentation:
This simple script minifies all python source files in the given directories: it removes line and block comments as well
as empty lines. All other files are simply copied to keep the folder structure. The script is tested for Ubuntu.

Usage:
Set one or more input directories, an output directory and a header for your files within the USER INPUT section.
Attention: The output folder is deleted during this process if it already exists!
"""

# ----------------------------------------------------------------------------------------------------------------------
# USER INPUT -----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# dirs_main_in = ["/TOP_PATH_TO_SOURCE_FILES/", "/TOP_PATH_TO_SOURCE_FILES_2/"]
# dir_main_out = "/OUTPUT_PATH/"
# header = "# Copyright 2019, NAME"

# example
dirs_main_in = ["~/GIT/mod_global_trajectory/"]
dir_main_out = "~/GIT/minified/"
header = "# Copyright 2019, Alexander Heilmeier"

# ----------------------------------------------------------------------------------------------------------------------
# PREPARATIONS ---------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# expand tilde to absolute path
for i, cur_entry in enumerate(dirs_main_in):
    dirs_main_in[i] = os.path.expanduser(cur_entry)
dir_main_out = os.path.expanduser(dir_main_out)

# delete output folder (if existing)
if os.path.exists(dir_main_out):
    rmtree(dir_main_out, ignore_errors=True)

# ----------------------------------------------------------------------------------------------------------------------
# LOOP THROUGH ALL DIRECTORIES/FILES -----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

for directory in dirs_main_in:

    # get current anchor directory index
    ind_anchor = directory[:-1].rfind("/") + 1

    for filepath_in in glob.iglob(directory + "**/*.*", recursive=True):

        # get current filename
        ind_filename = filepath_in.rfind("/") + 1
        filename = filepath_in[ind_filename:]

        # get current path starting with anchor directory
        rel_path_from_anchor = filepath_in[ind_anchor:ind_filename]
        dir_out = dir_main_out + rel_path_from_anchor

        # create output directory
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)

        # --------------------------------------------------------------------------------------------------------------
        # CASE 1: PY FILE ----------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        if filepath_in[-3:] == ".py":
            # open and read file line by line while editing lines
            with open(filepath_in, "r") as fh:
                text = ""                   # keeps the modified file content afterwards
                line = fh.readline()        # read first line
                in_block = False            # save if we are within a block comment

                while line:
                    # --------------------------------------------------------------------------------------------------
                    # BLOCK COMMENTS -----------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------

                    # find all """ within current line
                    ind_block = [m.start() for m in re.finditer("\'{3}|\"{3}", line)]

                    # if there is one """ then switch the in_block switch, if there are two delete line
                    if ind_block and len(ind_block) == 1:
                        if in_block:
                            line = ""
                            in_block = False
                        else:
                            in_block = True

                    elif ind_block and len(ind_block) == 2:
                        line = ""

                    # delete line if within a block comment
                    if in_block:
                        line = ""

                    # --------------------------------------------------------------------------------------------------
                    # LINE COMMENTS ------------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------

                    ind_hashtag = line.find("#")

                    # if hashtag exists and if there is no or only empty space before the hashtag remove the line
                    if ind_hashtag == 0 or (ind_hashtag > 0 and line[ind_hashtag - 1] == " "):
                        line = line[:ind_hashtag] + "\n"  # temporarily add a newline char because it was deleted before

                    # --------------------------------------------------------------------------------------------------
                    # REMOVE EMPTY LINES -------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------

                    line_temp = line.replace(" ", "")  # remove empty spaces temporary

                    if line_temp == "\n":
                        line = ""

                    # --------------------------------------------------------------------------------------------------
                    # ADD LINE TO TEXT ---------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------

                    # add line to text
                    text += line

                    # read next line
                    line = fh.readline()

            # ----------------------------------------------------------------------------------------------------------
            # WRITE MODIFIED TEXT --------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

            with open(dir_out + filename, "w") as fh:
                fh.write(header + "\n")
                fh.write(text)

        # --------------------------------------------------------------------------------------------------------------
        # CASE 2: OTHER FILE TYPE --------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        else:
            copyfile(filepath_in, dir_out + filename)

print("Minifying completed!")
