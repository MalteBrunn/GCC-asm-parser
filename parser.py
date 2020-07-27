#!/usr/bin/python3

import re
import sys
import subprocess

asm_identify_re = re.compile("^[ \t]*(?P<directive>\.)?(?P<command>[a-zA-Z0-9_]+)(?P<label>:)?[ \t]*(?(label)$|(?P<parameter>.+)?$)", re.M)

with open(sys.argv[1], "r") as handle:
  files = {}
  lastline = 0
  lastfile = 0
  for match in asm_identify_re.finditer(handle.read()):
    if not match.group('directive'):
      if match.group('label'):
        label = subprocess.run(["c++filt", match.group('command')], stdout=subprocess.PIPE).stdout.strip().decode('ascii')
        print("%s:"%label)
      else:
        print(files[lastfile], lastline, match.group(0))
    else:
      directive = match.group("command")
      parameter = match.group("parameter")
      if directive == "file" and parameter:
        decode = parameter.split()
        if len(decode) == 2:
          files[decode[0]] = decode[1].strip("\"")
      if directive == "loc" and parameter:
        decode = parameter.split()
        if len(decode) >= 2:
          lastline = decode[1]
          lastfile = decode[0]
