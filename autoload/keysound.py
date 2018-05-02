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
import os
import time
import pyglet


#----------------------------------------------------------------------
# AudioBank
#----------------------------------------------------------------------
class AudioBank (object):

	def __init__ (self):
		self._banks = {}
		self._insts = {}

	def load (self, filename):
		import pyglet
		filename = os.path.normcase(os.path.abspath(filename))
		if filename in self._banks:
			return self._banks[filename]
		audio = pyglet.media.load(filename, streaming = False)
		self._banks[filename] = audio
		return audio

	def play (self, filename):
		filename = os.path.normcase(os.path.abspath(filename))
		audio = self.load(filename)
		if filename not in self._insts:
			self._insts[filename] = []
		insts = self._insts[filename]
		found = None
		current = time.time()
		for inst in insts:
			if current >= inst.limit:
				found = inst
				break
		if found is None:
			if len(insts) >= 64:
				return False
			import pyglet
			found = pyglet.media.Player()
			insts.append(found)
		found.queue(audio)
		found.seek(0)
		found.play()
		found.startup = time.time()
		found.duration = audio.duration
		found.limit = found.startup + found.duration + 0.1
		return True


#----------------------------------------------------------------------
# load instance
#----------------------------------------------------------------------
audiobank = AudioBank()

def play(filename):
	return audiobank.play(filename)


#----------------------------------------------------------------------
# plugin 
#----------------------------------------------------------------------
def errmsg(text):
	import vim
	vim.tmp = text
	vim.command('call keysound#errmsg(s:pyeval("vim.tmp"))')


