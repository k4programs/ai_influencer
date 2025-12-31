# GEMINI Project Context

## Status Report
**Date**: 2025-12-31
**Phase**: Phase 10 (Advanced Personality) Complete
**Current Goal**: Maintenance & Monitoring.

## Architecture Decisions
- **Image Gen**: We use **Flux.1 [dev] fp8** locally for generation.
- **Control**: ComfyUI API + Python.
- **Training**: **Cloud Training (Civitai)**.
- **Intelligence**: **Ollama** (`mistral-nemo` 12B) for high-IQ responses, fact extraction, and creative direction.
- **Memory**: **User DB** (`user_db.json`) for long-term fact storage.
- **Automation**: **Instagrapi** for direct posting (Live) & DM/Comment handling.
- **Resource Mgmt**: **Sequential Execution** (Ollama -> Flux -> Upload) to prevent VRAM bottlenecks.

## User Preferences
- **Automation**: Always trigger workflows automatically via API.
- **Security**: Credentials in `.env` (gitignored).

## Completed Milestones
- [x] **Character Definition**: Defined "Lena-Marie" (Alpine DevOps).
- [x] **Visual Engine**: ComfyUI + Flux running locally.
- [x] **LoRA**: Trained & Verified (`lena_marie_v1_epoch_10.safetensors`).
- [x] **Intelligence**: Propals (3rd person) & Captions (1st person).
- [x] **Engagement**: DM Bot (Context-Aware) & Comment Bot.
- [x] **Live Deployment**: Profile Setup & First Post Executed.
- [x] **Advanced Intelligence**: Upgrade to `mistral-nemo` (12B).
- [x] **Long-Term Memory**: Fact extraction & storage (`user_db.json`).
- [x] **Visual DMs**: On-demand image generation in chat (`[SEND_PHOTO]`).
- [x] **Interactive Control**: CLI Menu System (`scheduler.py`).

## Next Steps
1.  **Voice**: Experiment with Audio-to-Text (Whisper) for DM inputs.
2.  **Stories**: Implement the Story Workflow (9:16) for daily "POV" updates.
3.  **Monitoring**: Observe "Ghost Mode" & Memory performance over time.
