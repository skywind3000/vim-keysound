#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# playsound2.py - play sound on Windows/OS X/Linux
#
# Created by skywind on 2018/05/02
# Last Modified: 2018/05/02 15:48:59
#
#======================================================================
from __future__ import print_function
import sys
import os
import time
import sdl2
import sdl2.sdlmixer


#----------------------------------------------------------------------
# 2/3 compatible
#----------------------------------------------------------------------
if sys.version_info[0] >= 3:
	long = int
	unicode = str
	xrange = range


#----------------------------------------------------------------------
# SDL2 sound
#----------------------------------------------------------------------
class AudioPlayback (object):

	def __init__ (self):
		if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
			raise RuntimeError("Cannot initialize audio system: {}".format(sdl2.SDL_GetError()))
		fmt = sdl2.sdlmixer.MIX_DEFAULT_FORMAT
		if sdl2.sdlmixer.Mix_OpenAudio(44100, fmt, 2, 1024) != 0:
			raise RuntimeError("Cannot open mixed audio: {}".format(sdl2.sdlmixer.Mix_GetError()))
		sdl2.sdlmixer.Mix_AllocateChannels(64)
		self._bank = {}

	def load (self, filename):
		filename = os.path.abspath(filename)
		uuid = os.path.normcase(filename)
		if uuid not in self._bank:
			if not isinstance(filename, bytes):
				filename = filename.encode('utf-8')
			sample = sdl2.sdlmixer.Mix_LoadWAV(filename)
			if sample is None:
				return None
			self._bank[uuid] = sample
		return self._bank[uuid]

	def play (self, sample, channel = -1):
		channel = sdl2.sdlmixer.Mix_PlayChannel(channel, sample, 0)
		if channel < 0:
			return None
		return channel

	def is_playing (self, channel):
		return sdl2.sdlmixer.Mix_Playing(channel)

	def set_volume (self, channel, volume = 1.0):
		if channel < 0:
			return False
		volint = int(volume * sdl2.sdlmixer.MIX_MAX_VOLUME)
		sdl2.sdlmixer.Mix_Volume(channel, volint)
		return True


#----------------------------------------------------------------------
# playsound
#----------------------------------------------------------------------
_playback = None

def playsound(path, volume = 1.0):
	global _playback
	if _playback is None:
		_playback = AudioPlayback()
	sample = _playback.load(path)
	if sample is not None:
		hr = _playback.play(sample)
		if hr >= 0:
			_playback.set_volume(hr, volume)
		return hr
	return None


#----------------------------------------------------------------------
# choose theme
#----------------------------------------------------------------------
def choose_theme(theme):
	for rtp in vim.eval('&rtp').split(','):
		path = os.path.join(rtp, 'themes')
	return ''


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':

	def test1():
		ap = AudioPlayback()
		print('haha')
		sp = ap.load("../sounds/typewriter/keyenter.wav")
		if not sp:
			print('bad sample')
		print('play: ', ap.play(sp))
		raw_input()
		print('play: ', ap.play(sp))
		raw_input()
		return 0

	def test2():
		while 1:
			for i in xrange(100):
				time.sleep(0.10)
				print(playsound('../themes/mario/keyany.wav'))
			print('stop ?')
			text = raw_input()
			if text == 'yes':
				break
		print('exit')
		raw_input()

	test2()

