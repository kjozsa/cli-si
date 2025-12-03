#!/usr/bin/env python3
import os
import sys

from loguru import logger
from openai import OpenAI

"""
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
"""


def generate_command_llm(prompt: str) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
    )
    logger.trace(f"LLM input prompt: {prompt!r}")
    system_prompt = (
        "You are an expert Linux shell user. "
        "Given a natural language request, output ONE shell command.\n"
        "Rules:\n"
        "- Output ONLY the command, no explanations.\n"
        "- Use standard Unix/Linux tools.\n"
        "- No markdown, no backticks, just plain text.\n"
        "- Make sure to use `sudo` for commands that require root privileges.\n"
        "- If the request is ambiguous or unclear, return # ERROR: <reason>.\n"
    )

    try:
        # model_name = "amazon/nova-2-lite-v1:free"
        # model_name = "mistralai/mistral-medium-3.1"
        # model_name = "gpt-3.5-turbo"
        model_name = "qwen/qwen3-vl-8b-instruct"
        # model_name = "deepseek/deepseek-v3.2-speciale"
        logger.trace(f"Calling LLM model: {model_name}")
        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=256,
            temperature=0.1,
        )
        logger.trace(f"Full message object: {resp.choices[0].message}")
        cmd = resp.choices[0].message.content.strip()
        cmd = cmd.replace("```", "").replace("shell\n", "").strip()
        logger.trace(f"LLM raw response: {resp}")
        logger.trace(f"LLM extracted command: {cmd!r}")
        return cmd
    except Exception as e:
        logger.error(f"LLM command generation failed: {e}")
        return f"# ERROR: LLM failed - {e}"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: si <natural language prompt>", file=sys.stderr)
        print("Example: si current date in iso format", file=sys.stderr)
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    print(generate_command_llm(prompt))


if __name__ == "__main__":
    main()
