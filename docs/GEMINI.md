# GEMINI Project Context

## Status Report
**Date**: 2025-12-31
**Phase**: Phase 8 (Live Deployment) Complete / Phase 9 (Scheduling & Voice) Active
**Current Goal**: 100% Autonomous Operation & Voice Interaction.

## Architecture Decisions
- **Image Gen**: We use **Flux.1 [dev] fp8** locally for generation.
- **Control**: ComfyUI API + Python.
- **Training**: **Cloud Training (Civitai)**.
- **Intelligence**: **Ollama** (Llama 3.2) for prompts (Visual), captions (Social) and DM replies.
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

## Next Steps
1.  **Scheduling**: Automate daily execution (Task Scheduler) to run without manual trigger.
2.  **Voice**: Experiment with Audio-to-Text (Whisper) for DM inputs.
3.  **Stories**: Implement the Story Workflow (9:16) for daily "POV" updates.
