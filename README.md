## doubler

Quick python script to simply extend lengths of aiff files while preserving pitch. Wrote as an exercise when I was stuck on a transcription and wanted to slow down a song. As of now it only works with mono files. Can be used from terminal or loaded as a module.

From terminal:


```
usage: doubler.py [-h] [-o OUTPUT] [-s SCALE] input

Scale mono AIFF files

positional arguments:
  input                 path to input AIFF file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        path to output AIFF file. Default is
                        [input]_x[scale].aiff
  -s SCALE, --scale SCALE
                        scale of output file. Scale=2 will produce output
                        twice as long. Must be a positive integer
```