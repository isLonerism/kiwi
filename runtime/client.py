#!/usr/bin/env python3

import os
import sys
import requests

def run(kiwi, args):

	# list modules
	if args.list_modules:
		installed = kiwi.get_installed_module_list()
			
		# try getting remote module list
		try:
			modules = kiwi.get_remote_module_list()
		except requests.exceptions.RequestException:
			kiwi.say("could not reach remote to fetch module list, listing local modules only")
			modules = installed[:]

		# compare modules and mark as installed
		for module in modules:
			print('[{}] {}: {}'.format('x' if module in installed else ' ', module, kiwi.get_module_description(module)))
			if module in installed:
				installed.remove(module)

		# list unknown modules
		for module in installed:
			print('[{}] {}: {}'.format('?', module, kiwi.get_module_description(module)))

	# fetching and updating modules have the same logic behind them
	elif args.get_modules or args.update_modules:
		modules = args.get_modules if args.get_modules else args.update_modules

		# fetching / updating all modules
		if 'all' in modules:
			if len(modules) > 1:
				kiwi.say("can't have 'all' argument with other modules listed")
				print("Possible solutions:")
				print("\t* kiwi {} all".format(sys.argv[1]))
				print("\t* kiwi " + sys.argv[1] + ' ' + ' '.join([module for module in modules if module != 'all']))
				sys.exit(1)
				
			# collect remote module list if fetching, local list if updating
			else:
				if args.get_modules:
					try:
						modules = kiwi.get_remote_module_list()
					except requests.exceptions.RequestException:
						kiwi.say("could not reach remote to fetch module list")
						sys.exit(1)
				else:
					modules = kiwi.get_installed_module_list()

		# fetch / update collected modules
		modules_fetched, modules_update, modules_failed = kiwi.fetch_modules(modules, args.update_modules != None)

		# fetch results
		if args.get_modules:
			kiwi.say('fetch results')
			print('\t* {} new modules fetched'.format(len(modules_fetched)))
			print('\t* {} modules could not be fetched'.format(len(modules_failed)))
			print('\t* {} modules have an available update'.format(len(modules_update)))
			if len(modules) != len(modules_fetched) + len(modules_update) + len(modules_failed):
				print('\t* {} modules are present and up to date'.format(len(modules) - len(modules_fetched) - len(modules_update) - len(modules_failed)))
	
		# update outdated modules if need be
		if len(modules_update) > 0:
			if kiwi.Helper.ask('Update the outdated modules?', ['y', 'n']) == 'y':
				modules_fetched, _, modules_failed = kiwi.fetch_modules(modules_update, True)
			else:
				sys.exit(0)

		# update results
		if args.update_modules or len(modules_update) > 0:
			kiwi.say('update results')
			print('\t* {} modules were updated'.format(len(modules_fetched)))
			print('\t* {} modules could not be updated'.format(len(modules_failed)))
	
	# kiwi self update
	elif args.self_update:

		if kiwi.runtime.update("I have an update"):
			kiwi.say("I'm up to date")
