# Agentic AI-Based Stow Space Optimization

## Backend Setup (Phase 1)

1. **Navigate to the backend directory** (optional, but requirements are in the root):
   ```bash
   cd stow-space-agent
   ```

2. **Create a Python Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your keys (especially `GROQ_API_KEY` for later phases). For Phase 1, we will use a local SQLite database for simplicity, which is configured by default.
   ```bash
   cp .env.example .env
   ```

5. **Run the Application**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

6. **Run Tests**:
   ```bash
   cd backend
   pytest tests/
   ```
