#!/usr/bin/env python

infile = "day1-input"

with open(infile, "rb") as fp:
    input = fp.read()

count = 0
basement = 0
for i, ch in enumerate(input):
    if ch == '(':
        count += 1
    elif ch == ')':
        count -= 1
    if basement == 0 and count == -1:
        basement = i+1

open_count = input.count("(")
close_count = input.count(")")

print "total chars:", len(input)
print "open count:", open_count
print "close count:", close_count
print "open - close:", open_count - close_count
print "net count:", count
print "basement:", basement

text = input.strip()
while "()" in text:
    text = text.replace("()", "")
while ")(" in text:
    text = text.replace(")(", "")

print "Stripped string:", text
print "length:", len(text)
