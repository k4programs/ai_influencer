# AI Influencer Project: Lena-Marie

**Status**: 🚧 Alpha / Development
**Tech Stack**: Python, ComfyUI (Flux.1), Ollama (LLM), Instagrapi (Automation)
**Documentation**: [Roadmap](docs/roadmap.md) | [Character Card](docs/character_card.md) | [Project Context](docs/GEMINI.md) | [Safety Report](docs/safety_report.md)

## Project Overview
This project aims to create a fully autonomous, realistic AI Influencer named **Lena-Marie** (21, Junior DevOps Engineer).
The system runs locally on a high-end PC (RTX 3080 Ti) and manages the entire content lifecycle from idea to Instagram post.

## Core Components
1.  **Visual Engine**: ComfyUI + Flux.1 [dev] (FP8) + Custom LoRA.
2.  **Intelligence Engine**: Ollama (Llama 3.2) for creative direction and caption writing.
3.  **Automation Layer**: Python scripts with `Instagrapi` for direct Instagram access.
4.  **Resource Manager**: Sequential execution logic to maximize VRAM usage.

## Getting Started

### Prerequisites
- Windows 10/11
- NVIDIA GPU with >= 12GB VRAM (for generation)
- Python 3.10+
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Ollama](https://ollama.com)

### Installation
1.  Clone repo.
2.  Create `.env` using `.env.template` and add Instagram credentials.
3.  See `docs/` for detailed setup guides.

### Usage (Automation)
**Run the full pipeline (Idea -> Image -> Post):**
```bash
# Edit scripts/auto_generate.py to set DRY_RUN = False for live posting
python scripts/auto_generate.py
```

## Directory Structure
- `brain/`: Knowledge base & task tracking.
- `ComfyUI/`: The specific ComfyUI instance (ignored by git).
- `docs/`: Setup guides and documentation.
- `scripts/`: Python helper scripts for API interaction.
- `training_data/`: Images for LoRA training.
- `workflows/`: JSON workflows for ComfyUI.
