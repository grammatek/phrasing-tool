Start with a normalized file, one sentence per line (such as lawnormalized.txt)

For tagged text, run:

```./icetagger.sh -i lawnormalized.txt -o lawtagged.txt -lf 2 -of 2```

where -i denotes the input file, -o the output file, -lf the line format and -of the output format (2 is for one sentence per line).

For parsed text, run:

```./iceparser.sh -i lawtagged.txt -o lawparsed.txt```

Finally, for phrasing, run:

```python phrasing.py lawparsed.txt lawphrased.txt```

You can see examples of all files in the Phrasing folder.
