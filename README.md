# rarbg-fix-subtitle-files

### Description

This script aims to clean and reorganize the `Subs` folder inside RARBG TV shows. On one hand, it cleans all the
subtitles files you don't need or want. On the other hand, the remaining subtitles are renamed to have the same filename
as its respective video file and moved to the same directory. 

With these two changes, media players, such as VLC, will automatically pick the right subtitle.

By default, the downloaded file structure looks like this:

```
.
├── Subs
│   ├── episode1
│   │   ├── 10_German.srt
│   │   ├── 2_English.srt
│   │   ├── 3_English.srt
│   │   ├── 4_English.srt
│   │   ├── 5_English.srt
│   │   ├── 6_Arabic.srt
│   │   ├── 7_Czech.srt
│   │   ├── 8_Danish.srt
│   │   └── 9_German.srt
│   └── episode2
│       ├── 10_German.srt
│       ├── 2_English.srt
│       ├── 3_English.srt
│       ├── 4_English.srt
│       ├── 5_English.srt
│       ├── 6_Arabic.srt
│       ├── 7_Czech.srt
│       ├── 8_Danish.srt
│       └── 9_German.srt
├── episode1.mp4
└── episode2.mp4
```

By running the script, the file structure will be as follows:

```
.
├── episode1.mp4
├── episode1.srt
├── episode2.mp4
├── episode2.srt
```

### Usage
Simply execute the script by running:
```commandline
python main.py
```

There are multiple arguments to customize the execution:
```commandline
usage: main.py [-h] [-l LANGUAGE] [-r]

options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Language for the subtitles you want, English by default e.g. --language=Spanish
  -r, --remove_subs_dir
                        use it if you want the `Subs` folder to be deleted when the script finishes
```
