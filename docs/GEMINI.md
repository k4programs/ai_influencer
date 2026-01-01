# GEMINI Project Context

## Status Report
**Date**: 2026-01-01
**Phase**: Phase 12 (Visual Automation / Physical Device)
**Current Goal**: Phase 13 (Story Content & Voice).

## Architecture Decisions
- **Image Gen**: We use **Flux.1 [dev] fp8** locally for generation.
- **Control**: ComfyUI API + Python.
- **Device**: **Huawei Mate 20 Pro** (Physical) via ADB.
- **Vision**: **Hybrid System**.
    - **OpenCV**: Precise UI interaction via Template Matching (Local).
    - **Gemini**: Semantic understanding (Context/Popups).
- **Intelligence**: **Unified Provider** (`llm_provider.py`). Primary: **Google Gemini** (`gemini-flash-latest`, Cloud). Fallback: **Ollama** (`mistral-nemo`, Local).
- **Memory**: **User DB** (`user_db.json`) for long-term fact storage.
- **Automation**: **Hybrid**:
    - **Physical**: `adb_client` for native Android app interaction (Ban Proof).
    - **API**: `Instagrapi` legacy fallback.
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
- [x] **Universal LLM Layer**: Hybrid Intelligence (Cloud + Local) with auto-switching.
- [x] **Live News Integration**: Auto-fetching TechCrunch/Heise via `news_manager.py`.
- [x] **Contextual Posts**: Hints & News Topics (`daily_hint.json`) drive content generation.
- [x] **One-Time Hints**: Automatic cleanup of prompts after posting.
- [x] **Brain 2.0 (Light)**: Topic Memory (`daily_topic.json`) for context-aware comments.
- [x] **Physical Device**: ADB Connection to Huawei Mate 20 Pro.
- [x] **Hybrid Vision**: OpenCV Template Matching + Gemini Fallback.
- [x] **Calibration**: Created Template Library (`assets/templates/`) for UI Icons.

## Next Steps
1.  **Stories**: Implement the Story Workflow (9:16) for daily "POV" updates.
2.  **Voice**: Experiment with Audio-to-Text (Whisper) for DM inputs.
3.  **Video**: Analyze Reels trend matching.
