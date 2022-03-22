Go to https://github.com/hrafnl/icenlp/releases, download IceNLP-1.5.0.zip and extract it into the current folder (Phrasing).

Start with a normalized file, one sentence per line (such as lawnormalized.txt)

```mv lawnormalized.txt IceNLP/bat/icetagger/```

```cd IceNLP/bat/icetagger```

You want your tagged text inside the parsing folder. Inside the icetagger folder, for tagged text, run:

```./icetagger.sh -i lawnormalized.txt -o ../iceparser/lawtagged.txt -lf 2 -of 2```

where -i denotes the input file, -o the output file, -lf the line format and -of the output format (2 is for one sentence per line).

Now enter the iceparser:

```cd ../iceparser```

You want your parsed file in the phrasing folder. For parsed text, run:

```./iceparser.sh -i lawtagged.txt -o ../../../lawparsed.txt```

Finally, for phrasing, run:

```cd ../../..```

```python phrasing.py lawparsed.txt lawphrased.txt```

You can see examples of all files in the Phrasing folder.
