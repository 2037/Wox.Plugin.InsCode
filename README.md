# Introduction
Tired of opening browser to access to ChatGPT for programming? Introducing InsCode, the ultimate time-saving plugin designed to streamline your experience with ChatGPT and revolutionize the way you generate code. InsCode empowers programmers with a simple and efficient solution to access ChatGPT and obtain quick answers to coding queries. 

With InsCode, you can now swiftly interact with ChatGPT to receive immediate assistance and generate code to your specific needs. Whether you're looking for quick facts, or simply seeking code suggestions, InsCode is your go-to companion for rapid development. 

This is a plugin of [Wox](https://github.com/Wox-launcher/Wox) in Windows. 

# Install
1. Clone the repo: `git clone https://www.github.com/2037/InsCode`
2. Unzip it to `%LOCALAPPDATA%\Wox\app-1.4.1196\Plugins` (change to your app version directory if needed)
3. Go to directory and install requirements: `pip install -r requirements.txt`
4. Get an OpenAI API key: https://platform.openai.com/account/api-keys
5. Open and insert your OpenAI API key to system environment. [Instruction](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) 

# Usage
1. Open Wox and type `i {question}` to ask your question (maybe ask for a helloworld program) in your favorite language. 
2. Paste it from clipboard or view it in Win+V if you use Win11. 
 
# Settings
Hit `Shift+Enter` after you type "i " to enter the context menu.

Set your instructions to GPT in `presets.json`. 

Set your prefered model in `preference.json`. The default model is *gpt-3.5-turbo*. The available models and their variants are [GPT3.5](https://platform.openai.com/docs/models/gpt-3-5), [GPT4](https://platform.openai.com/docs/models/gpt-4). Set your `max_token` to higher if needed (such like components in HTML). [Count Your Token Here](https://platform.openai.com/tokenizer). Set `is_keepitshort` to `false` to include explainations, default as `true` to only keep text in first code block. 

# Screenshots