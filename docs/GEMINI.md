# GEMINI Project Context

## Status Report
**Date**: 2025-12-31
**Phase**: Phase 5 (Social Media Setup) Complete / Phase 6 (Automation) Active
**Current Goal**: Full Automation - Live Instagram Deployment.

## Architecture Decisions
- **Image Gen**: We use **Flux.1 [dev] fp8** locally for generation.
- **Control**: ComfyUI API + Python.
- **Training**: **Cloud Training (Civitai)**.
- **Intelligence**: **Ollama** (Llama 3.2) for prompts (Visual) AND captions (Social).
- **Automation**: **Instagrapi** for direct posting (Mock/Live).
- **Resource Mgmt**: **Sequential Execution** (Ollama -> Flux -> Upload) to prevent VRAM bottlenecks.

## User Preferences
- **Automation**: Always trigger workflows automatically via API and notify upon completion.
- **Security**: Credentials in `.env` (gitignored).

## Completed Milestones
- [x] **Character Definition**: Defined "Lena-Marie" (Alpine DevOps).
- [x] **Visual Engine**: ComfyUI + Flux running locally.
- [x] **LoRA**: Trained & Verified (`lena_marie_v1_epoch_10.safetensors`).
- [x] **Intelligence**: Scripts for Propals (3rd person) & Captions (1st person).
- [x] **Automation**: `auto_generate.py` with sequential VRAM handling.
- [x] **Security**: Credential management via `.env`.

## Next Steps
1.  **Live Deployment**: Execute first real Instagram post.
2.  **Scheduling**: Automate daily execution (Task Scheduler/Cron).
3.  **Engagement**: Research comment-reply automation.
