import glob
import os
import numpy as np
from pathlib import Path
import shutil
import argparse


def main():
    args = parse_arguments()

    folders = glob.glob('./Subs/*')
    subs_to_move = []
    for f in folders:  # for each episode

        subs = glob.glob(f + "/*" + args.language.capitalize() + "*.srt")  # get list of subtitles matching language
        sizes = [os.path.getsize(f) for f in subs]  # get size of each subtitle file
        mean = np.mean(sizes)

        if len(sizes) > 2:
            # if there are more than 2 subtitles in the same language, the first is only foreign dialogues,
            # the last is audio description for deaf persons.
            # The ones in the middle are most likely to be a transcription of only the dialogues.
            # By doing the closest to the mean, it is ensured to pick the right one
            idx = (np.abs(np.asarray(sizes) - mean)).argmin()
            subs_to_move.append(subs[idx])
            continue

        if len(sizes) == 2:
            # if there are only two files, there are to scenarios:
            std = np.std(sizes)
            cv = std / mean
            if cv > 0.5:
                # the first being foreign language transcription and normal transcription.
                # This happens when the STD is high (one file has a small size and the other a big size).
                # Picking the bigger size one.
                idx = (np.abs(np.asarray(sizes) - mean)).argmax()
                subs_to_move.append(subs[idx])
            else:
                # the second being normal transcription and audio description for deaf person.
                # both files have similar size, and thus a lower std. Picking the smaller size one
                idx = (np.abs(np.asarray(sizes) - mean)).argmin()
                subs_to_move.append(subs[idx])
            continue

        if len(sizes) == 1:
            subs_to_move.append(subs[0])
            continue


    # rename and move files
    for sub in subs_to_move:
        parts = Path(sub).parts
        suffix = Path(sub).suffix
        shutil.copy(sub, "./" + parts[1] + suffix)

    # remove Subs folder and remaining files
    if args.remove_subs_dir:
        shutil.rmtree('./Subs')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', default='English',
                        help="Language for the subtitles you want, English by default e.g. --language=Spanish")
    parser.add_argument('-r', '--remove_subs_dir', default=False, action='store_true',
                        help='use it if you want the `Subs` folder to be deleted when the script finishes')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()

