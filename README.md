# "Chat with" Chatbot - WIP👋

Chat with different types of data/sources. Created with LangChain and Chainlit.

## Roadmap 🛣

Supported:

- [x] Text
- [x] PDF
- [x] HTML
- [x] CSV
- [ ] Website
- [ ] Github Repo
- [ ] Youtube Video
- [ ] Youtube Channel
- [ ] Podcast

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Installed a recent version of Python (3.7 or newer) installed and a way to create virtual environments (virtualenv or conda)
- Created OpenAI API account and obtain an API key

## Getting Started

Clone the repo

```bash
git clone https://github.com/waseemhnyc/Chat-with
```

Create a virutalenv and source the environment

```bash
python3 -m venv myenv
source venv/bin/activate
```

Install the necessary libraries

```bash
pip install -r requirements.txt
```

Create a .env file and input your OpenAI API Key in the file

```bash
cp .env.example .env
```

## Run locally

```bash
chainlit run app.py -w
```

## Deploy

WIP

## Questions or Get in Touch

[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/waseemhnyc)
[![Email](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:waseemh.nyc@gmail.com)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
