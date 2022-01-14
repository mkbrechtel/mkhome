function fish_title
  # Just calculate this once, to save a few cycles when displaying the prompt
  if not set -q __fish_prompt_hostname
    set -g __fish_prompt_hostname (hostname|cut -d . -f 1)
  end

  set -l suffix
  switch $USER
  case root toor
    set suffix '#'
  case '*'
    set suffix '>'
  end

  echo -n -s "$USER" @ "$__fish_prompt_hostname" : (prompt_pwd) " $suffix $_"
end
