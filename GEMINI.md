# GEMINI Project Context

## Status Report
**Date**: 2025-12-30
**Phase**: Phase 2 Completed (Visual Engine Setup)
**Current Goal**: Documentation & Dataset Generation.

## Architecture Decisions
- **Image Gen**: We use **Flux.1 [dev] fp8** because it fits into 12GB VRAM while offering state-of-the-art realism (better than SDXL).
- **Control**: We control ComfyUI via its **API (Port 8188)** using Python scripts, rather than writing custom nodes. This allows external orchestration (later n8n).
- **Training**: We decided on **Synthetic Data Generation**. We generate a dataset of ~20 images using a master prompt to then train a LoRA. This avoids legal/ethical issues of copying real people.

## Completed Milestones
- [x] **Character Definition**: Defined "Lena-Marie" (DevOps Nerd + Hiker).
- [x] **Roadmap**: Full project plan created.
- [x] **Infrastructure**: ComfyUI installed, Models downloaded.
- [x] **Integration**: Python scripts can trigger generation and retrieve images.

## Next Steps
1.  Generate Training Data (20 images).
2.  Train LoRA (likely using Kohya_ss).
3.  Install Ollama (Language Brain).
