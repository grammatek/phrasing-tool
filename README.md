# phrasing-tool
Tool for adding pauses in text for more natural speech.

To create the parsed text from the POS-tagged text:

```./iceparser.sh -i lawpos.txt -o law.txt```

To add pauses:

```python phrasing.py law.txt lawout.txt```
