# Utils for dealing with all my photos

## timelapse_stats.py

Reads through all the timelapse directories and reports the following stats:

```
Number of files: {Number}
Duration: {TimeDelta}
Size: {Human readable bytes} (Raw: {bytes})
Time taken: {Time taken for processing}
```

Assumes folders within the provided folders are of the structure:

```
YYYY-MM-DD Timelapse Title
├── Timelapse
│   ├── DSC_0001.nef
│   ├── DSC_0002.nef
│   ├── ...
```

## wall_paper_generator.py

Reads through all the photo directories and creates and output folder with new copies of photos in folders based on aspect ratio.

Outputs stats for the processing in the following format:

```
Number of photos created:
    Aspect Ratio: {Ratio} {Number of Photos}
    ...
Total number of photos: {Number}
Time taken: {Time taken for processing}
```

Assumes folders within the provided folders are of the structure:

```
YYYY-MM-DD Timelapse Title
├── Edits
│   ├── Output
|   │   ├── No watermark
│   |   |   ├── DSC_0001.jpg
│   |   |   ├── ...
```

## Caveats

- Intended to be run on windows (at time of writing python image info libraries not updated to python3)
- **Cannot be run through the python IDLE do to weirdness with stdout and multiprocessing**
  https://bugs.python.org/issue13220

## Todos

- exiv2 should be replaced with a better/more python library
- pass in directories instead of hardcoding them
