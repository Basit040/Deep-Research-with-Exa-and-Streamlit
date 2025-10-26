# Cerebras Deep Research 🧠

AI-powered research assistant that goes deeper than search. Built with Cerebras (fastest inference) and Exa (AI search engine).

![Demo](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## Features ✨

- 🔍 **Intelligent Web Search** - Uses Exa's neural + keyword search
- 📊 **Multi-Source Analysis** - Analyzes multiple sources simultaneously
- 🤖 **Three Research Modes**:
  - **Enhanced Research** - Two-layer deep dive with follow-up queries
  - **Multi-Agent Research** - Parallel specialized agents (Anthropic approach)
  - **Basic Research** - Single-layer quick analysis
- ⚡ **Fast Results** - Powered by Cerebras ultra-fast inference
- 🎨 **Modern UI** - Dark theme with Activity/Sources/Results tabs

## Quick Start 🚀

### 1. Installation

```bash
# Clone or download the repository
git clone <your-repo-url>
cd cerebras-deep-research

# Install dependencies
pip install streamlit exa-py cerebras-cloud-sdk
```

### 2. Get API Keys (Free!)

- **Cerebras API**: [https://cloud.cerebras.ai](https://cloud.cerebras.ai?utm_source=exademo)
- **Exa API**: [https://exa.ai](https://exa.ai/?utm_source=cerebras-research)

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 4. Configure & Research

1. Enter your API keys in the sidebar
2. Choose a research mode
3. Type your query or click an example prompt
4. Get comprehensive research results in seconds!

## Research Modes Explained 📚

### Enhanced Research (2-Layer)
- Initial broad search
- AI identifies knowledge gaps
- Targeted follow-up search
- Comprehensive synthesis

### Multi-Agent Research
- Lead agent decomposes query into subtasks
- Specialized subagents work in parallel:
  - Agent 1: Foundational aspects
  - Agent 2: Recent developments
  - Agent 3: Real-world applications
- Lead agent synthesizes all findings

### Basic Research
- Single search query
- Quick analysis
- Fast results

## Example Queries 💡

- "What are the most promising approaches to fusion energy?"
- "What are the latest developments in quantum computing?"
- "How can AI help solve climate change challenges?"
- "What are the current breakthroughs in biotechnology?"
- "Explain the state of autonomous vehicles in 2025"

## Project Structure 📁

```
cerebras-deep-research/
├── app.py                          # Main Streamlit application
├── build-your-own-perplexity.ipynb # Original Jupyter notebook
├── README.md                       # This file
└── requirements.txt                # Python dependencies (optional)
```

## How It Works 🔧

1. **Search**: Exa performs intelligent web search (neural + keyword)
2. **Extract**: Full content extracted from each source
3. **Analyze**: Cerebras LLM analyzes and synthesizes information
4. **Layer/Agent**: Additional searches based on gaps or parallel subtasks
5. **Synthesize**: Final comprehensive report with insights

## Technologies Used 🛠️

- **Streamlit** - Web framework
- **Cerebras Cloud SDK** - Ultra-fast LLM inference
- **Exa** - AI-powered search engine
- **Python 3.8+**

## Requirements 📋

```txt
streamlit>=1.28.0
exa-py>=1.16.1
cerebras-cloud-sdk>=1.56.1
```

## Tips for Best Results 💯

- Use specific, focused queries
- Try different research modes for different use cases
- Enhanced mode: Best for comprehensive deep dives
- Multi-Agent: Best for complex, multi-faceted topics
- Basic mode: Best for quick fact-finding
- Adjust number of sources based on topic complexity

## Contributing 🤝

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License 📄

MIT License - feel free to use for your own projects!

## Credits 🙏

Based on the Cerebras + Exa workshop: "Build Your Own Perplexity"

## Support 💬

- Cerebras Discord: [https://cerebras.ai/discord](https://cerebras.ai/discord)
- Issues: Open a GitHub issue

---

Built with ❤️ using Cerebras and Exa