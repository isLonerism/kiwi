#!/usr/bin/env python2
import distutils.spawn
import subprocess

lofi_url = "https://www.youtube.com/watch?v=hHW1oY26kxQ"

def main(args):
	if distutils.spawn.find_executable("explorer.exe") is not None:
		subprocess.call(["explorer.exe", lofi_url + "&\""])
	elif distutils.spawn.find_executable("xdg-open") is not None:
		subprocess.call(["xdg-open", lofi_url])
	else:
		print "No available browsers found."
