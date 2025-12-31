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
**Option A: One-Click Launcher (Recommended)**
Double-click `run_automation.bat` on your Desktop (create a shortcut).
- Opens a window and runs the Scheduler.
- 🛑 **To Stop**: Simply close the window (frees VRAM instantly).

**Option B: Manual (Terminal)**
```bash
# Run the complete scheduler loop
python scripts/scheduler.py

# Or singular scripts
python scripts/auto_generate.py
python scripts/reply_dms.py
```

## Directory Structure
- `brain/`: Knowledge base & task tracking.
- `ComfyUI/`: The specific ComfyUI instance (ignored by git).
- `docs/`: Setup guides and documentation.
- `output/`: Generated images (ignored by git).
- `scripts/`: Python helper scripts (`auto_generate`, `reply_dms`, `reply_comments`).
- `training_data/`: Images for LoRA training.
- `workflows/`: JSON workflows for ComfyUI.
