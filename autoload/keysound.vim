"======================================================================
"
" keysound.vim - 
"
" Created by skywind on 2018/05/01
" Last Modified: 2018/05/01 18:20:28
"
"======================================================================


"----------------------------------------------------------------------
" global settings
"----------------------------------------------------------------------
if !exists('g:keysound_py_version')
	let g:keysound_py_version = 0
endif

if !exists('g:keysound_theme')
	let g:keysound_theme = 'default'
endif


"----------------------------------------------------------------------
" tools
"----------------------------------------------------------------------
function! keysound#errmsg(msg)
	redraw | echo '' | redraw
	echohl ErrorMsg
	echom a:msg
	echohl NONE
endfunc


"----------------------------------------------------------------------
" python init 
"----------------------------------------------------------------------
let s:scripthome = expand('<sfile>:p:h')
let s:py_cmd = ''
let s:py_eval = ''
let s:py_version = 0

if g:keysound_py_version == 0
	if has('python')
		let s:py_cmd = 'py'
		let s:py_eval = 'pyeval'
		let s:py_version = 2
	elseif has('python3')
		let s:py_cmd = 'py3'
		let s:py_eval = 'py3eval'
		let s:py_version = 3
	else
		call keysound#errmsg('vim does not support +python/+python3 feature')
	endif
elseif g:keysound_py_version == 2
	if has('python')
		let s:py_cmd = 'py'
		let s:py_eval = 'pyeval'
		let s:py_version = 2
	else
		call keysound#errmsg('vim does not support +python feature')
	endif
elseif g:keysound_py_version == 3
	if has('python')
		let s:py_cmd = 'py3'
		let s:py_eval = 'py3eval'
		let s:py_version = 3
	else
		call keysound#errmsg('vim does not support +python3 feature')
	endif
endif

function! s:python(script)
	exec s:py_cmd a:script
endfunc

function! s:pyeval(script)
	if s:py_version == 2
		return pyeval(a:script)
	else
		return py3eval(a:script)
	endif
endfunc


"----------------------------------------------------------------------
" local init
"----------------------------------------------------------------------
call s:python('import sys')
call s:python('import os')
call s:python('import vim')
call s:python('import random')
call s:python('sys.path.append(vim.eval("s:scripthome"))')

let s:inited = 0
let s:themes = {}


"----------------------------------------------------------------------
" init import
"----------------------------------------------------------------------
function! s:init()
	if s:inited == 0
		call s:python('import keysound')
		let s:init = 1
	endif
endfunc


"----------------------------------------------------------------------
" play a sound
"----------------------------------------------------------------------
function! s:playsound(filename, ...)
	let s:volume = (a:0 > 0)? a:1 : 1000
	let s:filename = a:filename
	call s:init()
	call s:python('v = int(vim.eval("s:volume")) * 0.001')
	call s:python('keysound.playsound(vim.eval("s:filename"), v)')
endfunc


"----------------------------------------------------------------------
" choose_theme 
"----------------------------------------------------------------------
function! s:choose_theme(theme)
	for rtp in split(&rtp, ',')
		let s:path = fnamemodify(rtp, ':p')
		let s:join = 'sounds/' . a:theme
		let s:path = s:pyeval("os.path.join(vim.eval('s:path'), vim.eval('s:join'))")
		let s:path = s:pyeval("os.path.abspath(vim.eval('s:path'))")
		if isdirectory(s:path)
			return s:path
		endif
	endfor
endfunc


"----------------------------------------------------------------------
" play a sound in given theme
"----------------------------------------------------------------------
function! s:play(filename, ...)
	let theme = g:keysound_theme
	let volume = (a:0 > 0)? a:1 : 1000
	if has_key(s:themes, theme)
		let path = s:themes[theme]
	else
		let path = s:choose_theme(theme)
		let s:themes[theme] = path
	endif
	if path == ''
		call keysound#errmsg('ERROR: can not find theme "sounds/'. theme. '" folder in runtimepaths')
		return 
	endif
	let fn = path . '/' . a:filename
	if !filereadable(fn)
		call keysound#errmsg('ERROR: not find "'. a:filename.'" in "'.path.'"')
		return
	endif
	call s:playsound(fn, volume)
endfunc



"----------------------------------------------------------------------
" choose volume 
"----------------------------------------------------------------------
function! s:random(range)
	let s:range = a:range
	return s:pyeval('random.randint(0, int(vim.eval("s:range")))')
endfunc


function! keysound#play(key)
	let volume = 230 - s:random(50)
	if a:key == "\n"
		call s:play('keyenter.wav', volume)
	else
		call s:play('keyany.wav', volume)
	endif
endfunc


