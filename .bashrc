#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\[\e[36m\]\u@\h\[\e[0m\] \[\e[34m\]\W\[\e[0m\]]\$ '
