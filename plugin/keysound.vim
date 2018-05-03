"======================================================================
"
" keysound.vim - 
"
" Created by skywind on 2018/05/01
" Last Modified: 2018/05/01 18:21:05
"
"======================================================================


"----------------------------------------------------------------------
" internal state
"----------------------------------------------------------------------
let s:last_row = -1
let s:last_col = -1


"----------------------------------------------------------------------
" initialize
"----------------------------------------------------------------------
function! s:keysound_init(enable)
	if a:enable == 0
		augroup KeysoundEvents
			au!
		augroup END
	else
		augroup KeysoundEvents
			au! 
			au InsertEnter * call s:event_insert_enter()
			au TextChangedI * call s:event_text_changed()
			au TextChangedP * call s:event_text_changed()
		augroup END
	endif
endfunc

function! s:event_insert_enter()
	let s:last_row = line('.')
	let s:last_col = col('.')
endfunc

function! s:event_text_changed()
	let cur_row = line('.')
	let cur_col = col('.')
	if cur_row == s:last_row && cur_col == s:last_col + 1
		call keysound#play('c')
	elseif cur_row == s:last_row + 1 && cur_col == 1
		call keysound#play("\n")
	endif
	let s:last_row = cur_row
	let s:last_col = cur_col
endfunc

function! s:event_vim_enter()
endfunc


"----------------------------------------------------------------------
" commands
"----------------------------------------------------------------------
command! -nargs=0 KeysoundEnable call s:keysound_init(1)
command! -nargs=0 KeysoundDisable call s:keysound_init(0)

