# target format: user@host:~$
function fish_prompt --description 'prompt'
	# Just calculate this once, to save a few cycles when displaying the prompt
	if not set -q __fish_prompt_hostname
		set -g __fish_prompt_hostname (hostname|cut -d . -f 1)
	end

	set -l color_prompt
	set -l suffix
	switch $USER
	case root toor
		if set -q fish_color_cwd_root
			set color_prompt $fish_color_cwd_root
		else
			set color_prompt $fish_color_cwd
		end
		set suffix '#'
	case '*'
		echo -n -s "$USER" @
		set color_prompt $fish_color_cwd
		set suffix '>'
	end

  set -g fish_prompt_pwd_dir_length 0

	echo -n -s "$__fish_prompt_hostname" : (prompt_pwd) (set_color normal) " " (set_color $color_prompt) "$suffix "
end
