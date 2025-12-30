# AI Influencer Project: Lena-Marie

**Status**: 🚧 Alpha / Development
**Tech Stack**: Python, ComfyUI (Flux.1), Android (ADB), Ollama (LLM)
**Documentation**: [Roadmap](docs/roadmap.md) | [Character Card](docs/character_card.md) | [Project Context](docs/GEMINI.md)

## Project Overview
This project aims to create a fully autonomous, realistic AI Influencer named **Lena-Marie** (21, Junior DevOps Engineer).
The system runs locally on a high-end PC (RTX 3080 Ti) and controls a physical Android smartphone to post on Instagram.

## Core Components
1.  **Visual Engine**: ComfyUI + Flux.1 [dev] (FP8) for generating hyper-realistic images.
2.  **Intelligence Engine**: Ollama (Llama 3.2) for generating captions, comments, and personality.
3.  **Automation Layer**: Python + ADB to control the Instagram App on an Android device.
4.  **Orchestrator**: n8n (planned) to glue everything together.

## Getting Started

### Prerequisites
- Windows 10/11
- NVIDIA GPU with >= 12GB VRAM (for generation)
- Python 3.10+
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Ollama](https://ollama.com)

### Installation
See the `docs/` folder for detailed setup guides:
- [Setup ComfyUI](docs/setup_comfyui.md)
- [Setup Training (Cloud)](docs/cloud_training_guide.md)
- [Setup Intelligence](docs/setup_intelligence.md)

### Usage (Current)
**Visual Engine:**
```bash
python scripts/generate_image.py
```

**Intelligence Engine:**
```bash
ollama run llama3.2 "Say hi as Lena"
```
```bash
# Test connection to ComfyUI
python scripts/test_comfy.py

# Generate a test image
python scripts/generate_image.py
```

## Directory Structure
- `brain/`: Knowledge base & task tracking.
- `ComfyUI/`: The specific ComfyUI instance (ignored by git).
- `docs/`: Setup guides and documentation.
- `scripts/`: Python helper scripts for API interaction.
- `training_data/`: Images for LoRA training.
- `workflows/`: JSON workflows for ComfyUI.
