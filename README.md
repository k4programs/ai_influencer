# AI Influencer Project: Lena-Marie

**Status**: 🚧 Alpha / Development
**Tech Stack**: Python, ComfyUI (Flux.1), Ollama (`mistral-nemo`), Instagrapi (Automation)
**Documentation**: [Roadmap](docs/roadmap.md) | [Character Card](docs/character_card.md) | [Project Context](docs/GEMINI.md) | [Safety Report](docs/safety_report.md)

## Project Overview
This project aims to create a fully autonomous, realistic AI Influencer named **Lena-Marie** (21, Junior DevOps Engineer).
The system runs locally on a high-end PC (RTX 3080 Ti) and manages the entire content lifecycle from idea to Instagram post.

## Core Components
1.  **Visual Engine**: ComfyUI + Flux.1 [dev] (FP8) + Custom LoRA.
2.  **Intelligence Engine**: Ollama (`mistral-nemo` 12B) for high-level reasoning and conversation.
3.  **Memory System**: `memory_manager.py` builds an evolving dossier (`user_db.json`) for each user.
4.  **Automation Layer**: Python scripts with `Instagrapi`, controlled via a central **CLI Menu**.
5.  **Resource Manager**: Sequential execution logic to maximize VRAM usage.

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
Double-click `run_automation.bat` on your Desktop.
- Starts the **Interactive Menu**.
- Choose options via keys `[1]` to `[6]`.
- 🛑 **To Stop**: Press `Ctrl+C` in the window to return to the menu/exit.

**Option B: Manual (Terminal)**
```bash
# Run the Interactive Menu
python scripts/scheduler.py
```

### New Features (v2.0)
*   **Long-Term Memory**: Lena remembers facts about users (Jobs, Hobbies, etc.).
*   **Visual DMs**: Can send generated photos in chat if asked (`[SEND_PHOTO]`).
*   **Smart Online Status**: Simulates human online/offline patterns ("Ghost Mode").
*   **Security**: Sensitive user data is gitignored.

## Directory Structure
- `brain/`: Knowledge base & task tracking.
- `ComfyUI/`: The specific ComfyUI instance (ignored by git).
- `docs/`: Setup guides and documentation.
- `output/`: Generated images (ignored by git).
- `scripts/`: Python helper scripts (`auto_generate`, `reply_dms`, `reply_comments`).
- `training_data/`: Images for LoRA training.
- `workflows/`: JSON workflows for ComfyUI.
