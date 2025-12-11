si - shell interpreter powered by LLMs

This script translates natural language requests into shell commands using LLMs.
It's designed to be used in shell pipelines where the output is executed as a command.

Use it from fish like this: ~/.config/fish/functions/si.fish 
```
function si
    set cmd (python /home/kjozsa/workspace/ai/cli-si/si.py $argv)
    commandline --replace $cmd
    commandline -f repaint
end
```
