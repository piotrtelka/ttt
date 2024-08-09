#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

_ttt_completions() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="-rt -lo -o -f -lb -b -lt -t"

    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    if [[ ${prev} == "-o" ]]; then
        COMPREPLY=( $(compgen -W "$($SCRIPT_DIR/ttt_completion -o)" -- ${cur}) )
        return 0
    elif [[ ${prev} == "-b" ]]; then
        COMPREPLY=( $(compgen -W "$($SCRIPT_DIR/ttt_completion -b)" -- ${cur}) )
        return 0
    elif [[ ${prev} == "-t" ]]; then
        COMPREPLY=( $(compgen -W "$($SCRIPT_DIR/ttt_completion -t)" -- ${cur}) )
        return 0
    fi
}

complete -F _ttt_completions ttt
