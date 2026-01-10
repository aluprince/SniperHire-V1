Contributing to SniperHire-V1
First off, thank you for considering contributing to SniperHire! It's people like you that make SniperHire such a great tool for engineers.

🏗 Development Workflow
Fork the Repo: Create your own branch from main.

Setup Environment: Use a virtual environment (python -m venv .venv).

Coding Standards: - Use type hinting for all function signatures.

Follow PEP 8 style guidelines.

Ensure all CLI commands are documented via Typer's help parameter.

🧪 Testing
Before submitting a Pull Request, ensure:

The master_resume.json schema is preserved.

The CLI handles missing files gracefully.

The extraction logic handles diverse JD formats (markdown, raw text, etc.).

🗺 Feature Requests
We are specifically looking for help with Phase 2: Semantic Scoring. If you have experience with FAISS, ChromaDB, or high-dimensional embeddings, please open an issue to discuss your implementation strategy.