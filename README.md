# CliAI
> CliAI is a Python package that allows you to easily chat with OpenAI's ChatGPT using a command-line interface. With CliAI, you can quickly test and prototype new ideas, chatbots, and language models without writing a single line of code.

## Installation
You can install CliAI via pip:

```
pip install cliai
```

This program requires Python 3.8.
If for some reasons you do not want to mess up the old version system python, I recommend you to use tools like pyenv (e.g. `pyenv global 3.8.11`) to switch between versions.

## Usage
To start a conversation, simply run:

```
cliai chat
```
or alternatively `cliai converse`.

The CLI will guide you to create a configuration.
Alternatively, you can specify an API using `export OPENAI_API_KEY="your-key"` or using the `--api` flag.

## License
CliAI is distributed under the MIT license. See [LICENSE](./LICENSE) for more information.
