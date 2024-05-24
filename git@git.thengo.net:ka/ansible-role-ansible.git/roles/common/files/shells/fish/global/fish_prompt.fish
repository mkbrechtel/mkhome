function fish_prompt --description 'prompt'

	# Just calculate this once, to save a few cycles when displaying the prompt
	if not set -q __fish_prompt_hostname
		set -g __fish_prompt_hostname (hostname|cut -d . -f 1)
	end

	set -g fish_prompt_pwd_dir_length 0

	set -l prefix
	set -l suffix

	switch $USER
	case root toor
		set prefix (set_color -o brred)"$__fish_prompt_hostname"(set_color normal)(set_color -d '#AAAAAA')":"
		set suffix (set_color red)"#>"
	case '*'
		set prefix (set_color green)"$USER"(set_color normal)(set_color -d '#AAAAAA')"@"(set_color normal)(set_color -o white)"$__fish_prompt_hostname"(set_color normal)(set_color '#AAAAAA')":"
		set suffix (set_color green)">"
	end

	if [ "$XDG_SESSION_TYPE" != "x11" ]
		echo -n -s "$prefix"
	end

	echo -n -s (set_color normal)(set_color -o blue) (prompt_pwd) (set_color normal) " $suffix "

end
