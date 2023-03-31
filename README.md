# CliAI
![GitHub](https://img.shields.io/github/license/BaksiLi/CliAI)
![PyPI](https://img.shields.io/pypi/v/cliai?color=blue)
> CliAI is a user-friendly Python package that lets you interact with OpenAI's ChatGPT via a command-line interface (CLI). Easily test and prototype chatbots, language models, and innovative ideas without writing any code.

## Installation
Install CliAI using pip:
```
pip install cliai
```

CliAI requires Python 3.8 or higher.

## Usage and Tips
Start an interactive conversation by running:

```
cliai chat
```

The CLI will guide you through the process to create a configuration.

You can also specify an API key by setting the environment variable `export OPENAI_API_KEY="your-key"` or by using the `--api-key <OPENAI_API_KEY>` flag.

### Bypass OpenAI Restrictions
In certain regions (e.g., China), connecting to OpenAI may be problematic.
Bypass these restrictions by changing the official API base URL to a custom one using the `--api-base` flag.

```
cliai chat --api-base <OPENAI_API_BASE>
```

### Make it portable
You can use Linux on your mobile device to install CliAI.

For iOS & iPadOS, use iSH.

### Prompt Injection
During chat mode, you can easily modify messages. In addition to changing your own input (`user`), you can tweak the model's response (`assistant`) and system prompt (`system`) to guide the conversation as desired.
Also you can use [fine-tuning parameters](https://platform.openai.com/docs/api-reference/chat/create) to adjust the model's behaviour.

Experiment and enjoy hacking the model!

### Debugging
`--verbose`: Enable verbose output for easier debugging.
`--stream`: Enable stream output in the response (experimental).

## License
CliAI is distributed under the MIT license. See [LICENSE](./LICENSE) for more information.

To contribute to this project, feel free to raise issues or submit code.
