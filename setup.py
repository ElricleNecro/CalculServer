#! /usr/bin/env python3
# -*- coding:Utf8 -*-

#--------------------------------------------------------------------------------------------------------------
# All necessary import:
#--------------------------------------------------------------------------------------------------------------
import os, sys, glob

#from setuptools import find_packages
import setuptools as st
from distutils.core import setup
from distutils.command.install_data import install_data

packages = st.find_packages()

#--------------------------------------------------------------------------------------------------------------
# Call the setup function:
#--------------------------------------------------------------------------------------------------------------
setup(
	name        = 'CalculServer',
	version     = '0.1',
	description = 'Python Module for analysis gadget simulation on two different computer.',
	author      = 'Guillaume Plum',
	packages    = packages,
	cmdclass    = {'install_data': install_data},
	# data_files  = [
		# ('share/LibThese/animation-plugins', ["share/LibThese/animation-plugins/__init__.py"]), #glob.glob("share/LibThese/animation-plugins/*.py")),
	# ],
	scripts = [
		'scripts/cs_notifier.py',
		'scripts/cs_runner.py',
	],
)

#vim:spelllang=
