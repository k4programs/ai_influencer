# GEMINI Project Context

## Status Report
**Date**: 2025-12-30
**Phase**: Phase 3 (Training) & Phase 4 (Intelligence) Active
**Current Goal**: Training LoRA (Cloud) & Setting up Ollama.

## Architecture Decisions
- **Image Gen**: We use **Flux.1 [dev] fp8** locally for generation.
- **Control**: ComfyUI API + Python.
- **Training**: **Cloud Training (Civitai)**. We switched from local training (AI-Toolkit) to Cloud because 12GB VRAM/16GB RAM was insufficient for Flux LoRA training.
- **Intelligence**: **Ollama** running **Llama 3.2 (3B)** locally as the brain.

## Completed Milestones
- [x] **Character Definition**: Defined "Lena-Marie".
- [x] **Visual Engine**: ComfyUI + Flux running locally.
- [x] **Dataset**: 20+ High-Quality images generated & tagged.
- [x] **Training (Started)**: Dataset uploaded to Civitai, training in progress.
- [x] **Intelligence Engine**: Ollama installed, Llama 3.2 running.

## Next Steps
1.  Download finished LoRA from Civitai.
2.  Test LoRA in ComfyUI.
3.  Connect Python scripts with Ollama for automated captioning.
