# SSE Integration with LangGraph & React

This project uses **Server-Sent Events (SSE)** to provide real-time visualization of agent workflows.

## How it Works

1. **Backend (Python/FastAPI)**:
    - The API endpoint uses `StreamingResponse`.
    - It iterates over `graph.astream_events(..., version="v2")`.
    - Each event is wrapped in the SSE format: `data: {"type": "node_start", "node": "agent_name"}\n\n`.

2. **Frontend (React)**:
    - The UI uses the native `EventSource` API to connect to the backend.
    - As events arrive, the state of the **React Flow** graph is updated (e.g., highlighting active nodes).

## Running the Project

### Backend
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

## SSE Event Types
- `node_start`: Emitted when a LangGraph node begins execution.
- `node_end`: Emitted when a node completes, including the output data.
- `error`: Emitted if the workflow encounters an issue.
