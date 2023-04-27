# AI Devs Repository

This repository contains Python files for various tasks from AI / chatGPT training by https://www.aidevs.pl/ . In order to run any of the files from this repository, it is necessary to set up the following environment variables:

## Environment Variables

1. `URL_AI_DEVS`: This variable should point to the URL containing "zadania".
2. `AIDEVS`: Set this variable to your personal key provided by AI_DEVS.
3. `OPENAI_API_KEY`: This variable should be set to your OpenAI API key.

## Setting Environment Variables

### On Linux and macOS

Open your terminal and run the following commands:

```bash
export URL_AI_DEVS="https://tasks.com/"
export AIDEVS="your_personal_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
```

Or add an respective export to your ```~/.profile``` file


### On Windows

Open the Command Prompt or PowerShell and run the following commands:

<pre>
setx URL_AI_DEVS "https://example.com/zadania"
setx AIDEVS "your_personal_key_here"
setx OPENAI_API_KEY "your_openai_api_key_here"
</pre>

## Running a Python File
The name of each python file in the repository reflects the task (zadanie) name, it is designed to solve. To run a file, simply use the following command in your terminal or command prompt:

```bash
python task.py
```

Replace task.py with the name of the Python file you want to run.


## Optional Logging Parameter

Each module accepts an optional parameter, either DEBUG or INFO, to enable logging. To use this feature, pass the desired logging level as a command-line argument:

```bash
python task.py DEBUG
```

This will enable logging at the specified level (either DEBUG or INFO) while the script is running.
Empty paramter disables logging 