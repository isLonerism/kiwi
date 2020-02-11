#!/usr/bin/env python2

'''
Hi!

This is a general template for a kiwi module. Comments below will guide you around.
You copy this code, edit it, plug it into the module directory (/etc/kiwi/modules by default) and you're done.
I tried to keep it as minimal as possible. Have fun!

~ Lonerism
'''

# this optional variable is a list of kiwi modules that this module utilizes
# kiwi will read this list and fetch the missing modules before running this module
# a good example would be the 'journal' module which uses the 'storage' module
kiwi_dependencies = []

import argparse

# the basic requirement for a kiwi module is to have a kiwi_main() method
def kiwi_main():

	# docstrings are kiwi's module descriptions

	"""
	This module shows you all of the features kiwi provides to its modules.
	Should you wish to write your own module, use this module's code as a template:
	https://github.com/isLonerism/kiwi/blob/master/etc/kiwi/modules/helloworld.py
	"""

	# most kiwi modules use argparse, most also use docstring as description
	parser = argparse.ArgumentParser(description=kiwi_main.__doc__)
	parser.add_argument('-n', '--name', help='who should be greeted?', type=str)
	args = parser.parse_args()

	print "Hello, {}!".format(args.name if args.name else 'world')

	# bait the first time user to read the instructions	
	if not args.name:
		print 'Tip: use --help flag to see how you greet others!'