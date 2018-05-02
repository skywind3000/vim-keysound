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
import ctypes
import ctypes.wintypes


#----------------------------------------------------------------------
# mci interfaces
#----------------------------------------------------------------------
class WinMM (object):

	def __init__ (self):
		self.__winmm = ctypes.windll.winmm
		self.__mciSendString = self.__winmm.mciSendStringW
		LPCWSTR = ctypes.wintypes.LPCWSTR
		UINT = ctypes.wintypes.UINT
		HANDLE = ctypes.wintypes.HANDLE
		DWORD = ctypes.wintypes.DWORD
		self.__mciSendString.argtypes = [LPCWSTR, LPCWSTR, UINT, HANDLE]
		self.__mciSendString.restype = ctypes.wintypes.DWORD
		self.__mciGetErrorStringW = self.__winmm.mciGetErrorStringW
		self.__mciGetErrorStringW.argtypes = [DWORD, LPCWSTR, UINT]
		self.__mciGetErrorStringW.restype = ctypes.wintypes.BOOL
		self.__buffer = ctypes.create_unicode_buffer(2048)
		self.__alias_index = 0

	def mciSendString (self, command, encoding = None):
		if encoding is None:
			encoding = sys.getfilesystemencoding()
		if isinstance(command, bytes):
			command = command.decode(encoding)
		hr = self.__mciSendString(command, self.__buffer, 2048, 0)
		if hr != 0:
			return long(hr)
		text = self.__buffer.value
		return text

	def mciGetErrorString (self, error):
		buffer = self.__buffer
		hr = self.__mciGetErrorStringW(error, buffer, 2048)
		if hr == 0:
			return None
		return buffer.value


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':

	def test1():
		mci = WinMM()
		print(mci.mciGetErrorString(1))
		return 0


	test1()

