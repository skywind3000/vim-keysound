#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# keysound.py - 
#
# Created by skywind on 2018/05/01
# Last Modified: 2018/05/01 20:33:59
#
#======================================================================
import sys
import time
import pyglet


#----------------------------------------------------------------------
# plugin 
#----------------------------------------------------------------------


def errmsg(text):
	import vim
	vim.tmp = text
	vim.command('call keysound#errmsg(s:pyeval("vim.tmp"))')


