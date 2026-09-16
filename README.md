# L.A. Noire Interactive Partner (Bekowsky AI)

A state-aware, locally-hosted LLM roleplay partner inspired by *L.A. Noire*. Built with Python, SQLite, and Ollama (`llama3.2:1b`).

## Features
- **Desk-Aware Personas:** Dynamic prompts across Traffic, Homicide, Vice, and Arson desks.
- **Interactive Notebook:** SQLite-backed command system (`/note`, `/notes`, `/clear`) that injects dynamic context into the LLM prompt.
- **Character Lock:** Strict persona preservation with 1940s detective dialect.

## Prerequisites
- Python 3.8+
- [Ollama](https://ollama.com/) running locally with `llama3.2:1b`:
  ```bash
  ollama pull llama3.2:1b

