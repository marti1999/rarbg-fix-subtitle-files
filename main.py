import glob
import os
import numpy as np
from pathlib import Path
import shutil
import argparse

def main():

    # get list of subtitles files in the desired language
    all_files = set(glob.glob('./Subs/**/*.srt', recursive=True))
    excluded_files = set(glob.glob('./Subs/**/*English*', recursive=True))
    to_remove_files = list(all_files - excluded_files)

    # remove files in another language
    for file in to_remove_files:
        try:
            # os.remove(file)
            print(str(file))
        except OSError:
            print("error")

    # from all the subtitles in our language, discard the ones with only foreign dialogues or audio descriptive
    folders = glob.glob('./Subs/*')
    subs_to_move = []
    for f in folders:
        subs = glob.glob(f+"/*")
        sizes = [os.path.getsize(f) for f in subs]
        mean = np.mean(sizes)

        if len(sizes) > 2:
            idx = (np.abs(np.asarray(sizes)-mean)).argmin()
            subs_to_move.append(subs[idx])
            continue
        if len(sizes) == 2:
            std = np.std(sizes)
            cv = std / mean
            if cv > 0.5:
                idx = (np.abs(np.asarray(sizes)-mean)).argmax()
                subs_to_move.append(subs[idx])
            else:
                idx = (np.abs(np.asarray(sizes) - mean)).argmin()
                subs_to_move.append(subs[idx])
            continue
        if len(sizes) == 1:
            subs_to_move.append(subs[0])

    # rename and move files
    for sub in subs_to_move:
        parts = Path(sub).parts
        suffix = Path(sub).suffix
        os.rename(sub, "./"+parts[1]+suffix)

    # remove Subs folder and remaining files
    shutil.rmtree('./Subs')



if __name__ =="__main__":
    main()