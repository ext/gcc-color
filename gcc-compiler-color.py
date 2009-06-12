#!/usr/bin/env python

#
# Copyright (c) 2009, David Sveningsson <ext-spamtag@sidvind.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import sys, os, subprocess

path, compiler = os.path.split(sys.argv[0])
if compiler[-5:] == 'color':
	compiler = compiler[:-6]

filter = True
if 'NOCOLOR' in os.environ:
	# don't filter if the variable is set to y*
	if os.environ['NOCOLOR'][0] == 'y':
		filter = False

	# don't filter if the variable is set to true
	if os.environ['NOCOLOR'] == 'true':
		filter = False

argv = [compiler] + sys.argv[1:]

p = subprocess.Popen(args=argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.getcwd(), env=os.environ, shell=False)

while(p.returncode == None):
	stdout, stderr = p.communicate()

stdout_lines = stdout.split("\n")

if filter:
	for line in stdout_lines[:-1]:
		tokens = line.split(' ')
		if tokens[1] in ['fel:', 'error:']:
			print "\033[01;31m" + line + "\033[0m"
			status = 2
		elif tokens[1] in ['varning:', 'warning:']:
			print "\033[01;33m" + line + "\033[0m"
		else:
			print line
else:
	for line in stdout_lines[:-1]:
		print line

sys.exit(p.returncode)
