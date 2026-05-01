# UI Automation Agent (Android CLI Edition)
This repository contains an intelligent Android UI automation framework that replaces traditional OCR with direct Android CLI layout parsing. It uses an LLM-powered agent to handle complex navigation sequences, specifically designed for "Agentic Orchestration" on local Windows machines.  

**Key Features:**
-Direct Layout Parsing: Uses android layout -p to fetch the UI tree, eliminating the "halucinations" common with OCR-based detection.  

-Agentic Orchestration: Uses a "Reason-Act-Observe" loop where the LLM decides which buttons to click based on the current UI state.  

-Repetitive Workflow: Built-in support for executing multi-step cycles (e.g., Home → Favorites → Profile) multiple times.  

-Gemma 4 Integration: Optimized for the gemma4:e4b model via Ollama for high-speed local reasoning on 32GB RAM laptops.

