function aptitude-list-manually-installed --description 'list all manually installed packages without system packages'
  aptitude search '!?priority(required) !?priority(important) ?installed !?automatic' $argv
end

function apt-tail-log --description 'tail the apt log'
  tail -f /var/log/apt/term.log $argv
end
