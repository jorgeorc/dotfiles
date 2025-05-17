autoload -Uz compinit promptinit
compinit
promptinit
autoload -Uz zle

# Set custom prompt
PS1="%F{green}%n@%m%f:%F{red}%~%f %F{white}%#%f "
alias ls='eza --group-directories-first'
alias tree='eza -T'

# Set completion style
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'
neofetch
