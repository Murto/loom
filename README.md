# Loom

Loom is a programming language for playing around with sets and strings,
focusing on the implementations of set and string operations with regards to
formal language theory.

## Example

The following example is available under `example`:

```
# Define language of 0 and 1 (binary string alphabet)
bits := {0, 1}

# Define ascii character language
ascii := bits × bits × bits × bits × bits × bits × bits × bits

# Get ascii input
input ∈ ascii* ?

# Define L, o, and m ascii characters
L := 01001100 ∈ ascii
o := 01101111 ∈ ascii
m := 01101101 ∈ ascii

# Concatenate ascii characters to make binary string
# representing "Loom"
Loom := L + o + o + m ∈ ascii × ascii × ascii × ascii

colon := 00111010 ∈ ascii

# Print loom in binary
Loom + colon + input !

```

## Continuous Integration

| Branch  | Status                                                                                                   |
| ------- |:--------------------------------------------------------------------------------------------------------:|
| master  | [![Build Status](https://travis-ci.org/Murto/loom.svg?branch=master)](https://travis-ci.org/Murto/loom)  |
| develop | [![Build Status](https://travis-ci.org/Murto/loom.svg?branch=develop)](https://travis-ci.org/Murto/loom) |
