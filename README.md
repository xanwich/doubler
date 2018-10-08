## doubler

Quick python script to simply extend lengths of aiff files while preserving pitch. Wrote as an exercise when I was stuck on a transcription and wanted to slow down a song. Can be used from terminal or loaded as a module.

The files this creates sound pretty bad as a result of the simple algorithim. Better pattern matching could be used to create more convincing output. However, these results sound interesting at large numbers (scale > 25) and could be potentially useful in studying overtones. But since it outputs uncompressed audio files, this creates very large files.

From terminal:

```
usage: doubler.py [-h] [-o OUTPUT] [-s SCALE] [-c CHANNEL] input

Scale AIFF files

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
  -c CHANNEL, --channel CHANNEL
                        channel from which to determine waveforms to repeat
```