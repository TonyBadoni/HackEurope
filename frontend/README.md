# Frontend - Real-time Updates with SSE

React + Vite frontend application with Server-Sent Events (SSE) for receiving real-time updates from the backend.

## Tech Stack

- **React 19.2** - UI library
- **Vite 8** - Build tool and dev server
- **Server-Sent Events (SSE)** - Real-time server-to-client updates

## Development

```bash
npm install
npm run dev
```

## SSE Implementation Plan

### Overview
The frontend will use the EventSource API to receive real-time updates from the backend via Server-Sent Events (SSE). This allows the server to push multiple updates to the client over a single HTTP connection.

### Architecture

#### 1. **SSE Service** (`src/services/sseService.js`)
Create a reusable service to manage SSE connections:

```javascript
// Handle connection, reconnection, and error management
// Provide event listeners for custom event types
// Auto-reconnect with exponential backoff on disconnection
```

**Features:**
- Connection state management (connecting, connected, disconnected, error)
- Automatic reconnection with configurable retry logic
- Support for multiple event types
- Cleanup on component unmount

#### 2. **Custom React Hook** (`src/hooks/useSSE.js`)
Create a React hook for easy SSE integration in components:

```javascript
const { data, status, error } = useSSE('/api/stream-endpoint', options);
```

**Returns:**
- `data`: Array of received messages/updates
- `status`: Connection status
- `error`: Error message if connection fails
- `disconnect()`: Manual disconnect function

#### 3. **Component Integration**

**Example: Real-time Dashboard**
```jsx
function Dashboard() {
  const { data, status } = useSSE('/api/events', {
    onMessage: (event) => {
      // Handle incoming message
    },
    onError: (error) => {
      // Handle error
    }
  });
  
  return (
    <div>
      <StatusIndicator status={status} />
      <UpdatesList updates={data} />
    </div>
  );
}
```

### Event Types

The backend can send different event types:

1. **`message`** - Default event type (generic updates)
2. **`progress`** - Progress updates (e.g., processing status)
3. **`notification`** - User notifications
4. **`data`** - Data updates (e.g., new records)
5. **`error`** - Error messages from server

### Implementation Steps

#### Phase 1: Core SSE Infrastructure
- [ ] Create `src/services/sseService.js` with EventSource wrapper
- [ ] Implement connection management and error handling
- [ ] Add reconnection logic with exponential backoff

#### Phase 2: React Integration
- [ ] Create `src/hooks/useSSE.js` custom hook
- [ ] Implement state management for messages and connection status
- [ ] Add cleanup logic for component unmount

#### Phase 3: UI Components
- [ ] Create `ConnectionStatus` component (visual indicator)
- [ ] Create `UpdatesList` component (display received updates)
- [ ] Create `Notification` component (show notifications)

#### Phase 4: Error Handling & UX
- [ ] Implement user-friendly error messages
- [ ] Add loading states during connection
- [ ] Display reconnection attempts
- [ ] Add manual reconnect button

#### Phase 5: Testing & Optimization
- [ ] Test connection stability
- [ ] Test reconnection scenarios
- [ ] Optimize re-renders
- [ ] Add message buffering if needed

### Best Practices

1. **Connection Management**
   - Always close EventSource connections on component unmount
   - Implement reconnection logic for network failures
   - Handle browser tab visibility (pause/resume connections)

2. **Performance**
   - Use React.memo() for update components to prevent unnecessary re-renders
   - Implement message buffering for high-frequency updates
   - Limit stored message history to prevent memory leaks

3. **Error Handling**
   - Show user-friendly error messages
   - Log errors for debugging
   - Provide manual reconnect option
   - Handle timeout scenarios

4. **Security**
   - Use HTTPS in production for encrypted connections
   - Implement authentication tokens in request headers
   - Validate server messages before processing

### Backend Endpoint Requirements

The backend should provide SSE endpoints that:
- Return `Content-Type: text/event-stream`
- Send keep-alive comments every 15-30 seconds
- Support CORS for development
- Include event IDs for message tracking
- Format: `event: <type>\ndata: <json>\nid: <id>\n\n`

### Example Backend Response Format

```
event: notification
data: {"message": "New update available", "timestamp": 1234567890}
id: 1

event: progress
data: {"percentage": 50, "status": "processing"}
id: 2

event: data
data: {"records": [...], "count": 10}
id: 3
```

## Directory Structure

```
src/
├── components/
│   ├── ConnectionStatus.jsx    # Connection status indicator
│   ├── UpdatesList.jsx         # Display SSE updates
│   └── Notification.jsx        # Toast notifications
├── hooks/
│   └── useSSE.js               # Custom SSE hook
├── services/
│   └── sseService.js           # SSE connection management
└── utils/
    └── formatters.js           # Message formatting utilities
```

## Configuration

Environment variables (`.env`):
```env
VITE_API_URL=http://localhost:8000
VITE_SSE_RECONNECT_ATTEMPTS=5
VITE_SSE_RECONNECT_DELAY=1000
```

## Resources

- [MDN EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [React SSE Best Practices](https://react.dev/learn/synchronizing-with-effects#fetching-data)
