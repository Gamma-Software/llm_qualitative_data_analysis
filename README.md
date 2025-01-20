# Qualitative Data Analysis 📝
This is a tool to help you do your qualitative data analysis. 🧐
This can for instance take your transcripts and generate codes and themes for you 💡. It summarizes your data and can help you get insights on your data. 📊

# 🔬 Tech stack
The Qualitative Data Analysis uses [LLMs](https://en.wikipedia.org/wiki/Large_language_model) or Large Language Models to generate the summary / codes / themes and classify them. 🤖
The application is developped with Python.

## Python Libraries
This tool is powered by libraries:
- [Streamlit](https://streamlit.io): For the User Interface 🖥️
- [Langchain](https://langchain.com): For creating LLMs applications 🔗
- [OpenAI](https://openai.com): The LLMs provider. For now we only integrated this LLM.

# Getting started 🏁

## Requirements

You need to have [Python](https://www.python.org/downloads/) installed on your computer.
Choose the latest version of Python 3. 🐍. The version tested is 3.8.10.

## Configuration

Rename the `.streamlit/secrets_template.toml` file to `.streamlit/secrets.toml` and edit it to add your own configuration about langchain, langsmith and openai api key.

## Installation

Clone the repository and install the dependencies:

```bash
git clone
cd qualitative-data-analysis
sudo ./scripts/getting_started.sh
```

The getting_started.sh script will ask you for your OpenAI API key and will create the secrets.toml file for you.

## Run the application

```bash
streamlit run source/qualitative_analyse_agent.py
```

# Usage 📖

The usage is pretty simple. 🤓

1. Upload your transcripts: You can upload your transcripts from the sidebar 📂.
    - Generate transcripts summary: In the Raw data section, you can generate a summary of your data individually.
2. Enter your research question: You can enter your research question. This will be used to generate codes and themes. ❓
3. Generate codes and themes: You can now click on the button to generate codes and themes. This will generate codes and themes based on your research question. 💡

# Langsmith integration 🔗

You can use langsmith to monitor your application and get insights on how it is used. 📊

Edit the `.streamlit/secrets.toml` file and add the following lines:

```toml
[langsmith]
tracing = true
api_url = "https://api.smith.langchain.com"
api_key = "your key here"
project = "your project here"
```

# Diagrams
## Libs
TODO Show a diagram with the interaction between libs

## LLM chain
TODO show the LLM Chaining

# Features ✨
- Upload your transcripts 📂
- Generate Summary on all data or on a specific data 📊
- Based on a research question generate a summary of the data, generate codes and themes. ❓
- Update Qualitative Analysis Data parameters 🔄
- Generate a Qualitative Data Analysis report and download it 📄

# Limitations ⚠️
- For now, the tool cannot perform a Qualitative Data Analysis on large datasets as the LLM used is limited to 16000 tokens. 🚫
- The data is not cached and the report as well. So if you reset the page the data will have to be uploaded and the report regenerated again. 🔄

# Improvements 🚀
- Upload voice transcripts and convert them to text and perform a Qualitative Data Analysis 🗣️
- Connect to Qualitative Data softwares 🤝
- (double check) Do intermediates checkings on the results to avoid LLM bias 🤔
- Perform map-refine summary on the data
- Handle large data transcripts

# Background 🧑‍🎓
My name is [Valentin Rudloff](https://www.linkedin.com/in/rudloffvalentin/) and I'm a Engineer. I make stuff in various fields. 👨‍🔧
For my wife's memoire, she needed a tool to help her do a Qualitative Data Analysis on transcripts she conducted. 📚
LLMs are really good at understanding human semantics and thus perform a Qualitative Data Analysis. 🧠
This application helped her get almost an instant result, and I'm pretty sure this can help you as well. 👍

# Acknowledgements 🙏
The application and the LLM prompt are greatly inspired by Dr. [Philip Adu, Ph.D](https://www.drphilipadu.com) video [Master Qualitative Data Analysis with ChatGPT: An 18-Minute Guide](https://www.youtube.com/watch?v=L1WelrcgLGM).

Made with ❤️ by [Valentin Rudloff](https://www.linkedin.com/in/rudloffvalentin/)
If you want to help me create other stuff like this you can [buy me ☕](https://www.buymeacoffee.com/valentinrudloff)