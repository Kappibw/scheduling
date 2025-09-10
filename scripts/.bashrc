# ~/.bashrc - dev-friendly defaults

# If not running interactively, don’t do anything
[[ $- != *i* ]] && return

# ----- Prompt -----
# Show user@host, cwd, and git branch in color
parse_git_branch() {
  git branch 2>/dev/null | sed -n '/\* /s///p'
}
export PS1="\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\]\$ "

# ----- Color support -----
if command -v dircolors >/dev/null 2>&1; then
  eval "$(dircolors -b)"
fi

alias ls='ls --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# ----- History -----
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoredups:erasedups
shopt -s histappend
PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"

# ----- Useful defaults -----
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias gs='git status'
alias gd='git diff'
alias gc='git commit'
alias gp='git push'

# ----- Completion -----
if [ -f /etc/bash_completion ]; then
  . /etc/bash_completion
fi

# ----- Extra safety -----
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# ----- Python -----
alias ipy='ipython'
