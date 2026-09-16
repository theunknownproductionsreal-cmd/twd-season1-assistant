# The Walking Dead Season 1 Terminal Assistant

A local, terminal-based AI companion built for **Termux** that pairs a lightweight LLM (`llama3.2:1b`) with a SQLite database to deliver pragmatic survival advice and real Telltale choice statistics without hallucinating gameplay data or medical fanfiction.

## Why a Hybrid Architecture?
1-billion parameter models are great for running locally on a phone, but they fail miserably at math and consistency. This project decouples data from persona:
- **SQLite (`twd_stats.db`)**: Holds immutable, accurate player choice percentages and episode data.
- **Ollama (`llama3.2:1b`)**: Handles the Lee Everett roleplay layer, keeping the tone grounded, weary, and tactical.

## Features
- **Lee Everett Persona:** Pragmatic, grounded group survival guidance.
- **Choice Statistics (`/episodes`):** Fetches real global Telltale player percentages straight from the local database instead of inventing them.
- **Guardrailed Logic:** Keeps the model focused on group dynamics and tactical choices rather than pretending it's an ER doctor.

## Prerequisites
- Termux environment on Android
- Python 3.x with built-in `sqlite3`
- [Ollama](https://ollama.com/) running locally with `llama3.2:1b` pulled.

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/twd-season1-assistant.git](https://github.com/YOUR_USERNAME/twd-season1-assistant.git)
   cd twd-season1-assistant

