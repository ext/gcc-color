#!/usr/bin/python
import sys, os, subprocess

path, compiler = os.path.split(sys.argv[0])
if compiler[-5:] == 'color':
	compiler = compiler[:-6]

filter = True
if 'NOCOLOR' in os.environ:
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
