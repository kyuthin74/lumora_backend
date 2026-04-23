# WebSocket Chat with Gemini AI and Session History

## Overview
Build a WebSocket endpoint using FastAPI + Gemini AI SDK that supports multi-turn conversations. Each user has ONE persistent chat history that accumulates messages across WebSocket connections. On disconnect, save all messages to the `ChatHistory` table in PostgreSQL. On new connection, retrieve and pre-load all historical messages to provide continuity.

## Implementation Steps

### Phase 1: Database & Models
1. Create `ChatHistory` model in `app/models/chat_history.py` with fields:
   - `id` (primary key)
   - `user_id` (FK to User, unique constraint - one chat history per user)
   - `messages` (JSON array of all conversation messages across all sessions)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)
   - Relationship to User

2. Generate Alembic migration file to create `chat_history` table with:
   - Unique index on `user_id`
   - Index on `created_at`

3. Create CRUD operations in `app/crud/chat_history.py` with functions:
   - `create_or_get_user_history()` — get or create single chat history for user
   - `update_chat_history()` — append/update messages for user
   - `get_user_chat_history()` — retrieve all messages for a user

### Phase 2: Dependencies & Service Layer
4. Update `requirements.txt` to add:
   - `google-generativeai` package

5. Update `app/config.py` to add:
   - Gemini API key configuration (from environment variable)

6. Update `app/services/chatbot_service.py` to:
   - Replace OpenAI with Gemini AI SDK
   - Implement `init_gemini_chat()` — initialize chat session with full history loaded
   - Implement `get_chat_response()` — send message, return response
   - Keep personality/context building logic from current implementation (mood context, risk score, etc.)

### Phase 3: WebSocket Endpoint & Session Management
7. Create new WebSocket handler in `app/api/chatbot.py` with endpoint:
   - `GET /ws/chatbot` (authenticated via token in query string or header)
   - Extract `user_id` from auth token (using existing security utilities)

8. Implement connection lifecycle (all async):
   - **On connect**:
     - Authenticate token, extract user_id
     - Load user's existing chat history via `get_user_chat_history(user_id)`
     - Initialize Gemini chat session with all previous messages
     - Add to active connections set
   - **On message**:
     - Send to Gemini
     - Stream/await response
     - Send back to client
   - **On disconnect**:
     - Call `chat.get_history()` from Gemini SDK
     - Update user's chat history via `update_chat_history()` with all accumulated messages
     - Remove from active connections set

9. Implement proper error handling:
   - Authentication errors (invalid/expired token)
   - Connection errors
   - Gemini API errors (quota, timeout, etc.)
   - Reconnection logic
   - Connection pooling/limits (1 active connection per user recommended)

### Phase 4: Integration & Context
10. Update User model relationship to include `chat_history` backref for easy queries

11. Ensure personality/mood context is preserved:
    - Fetch recent mood entry
    - Fetch latest risk score
    - Fetch 30-day mood statistics before initializing chat session
    - Include this context in Gemini system prompt

12. Remove or deprecate the old REST `POST /chatbot/messages` endpoint (if compatibility not needed)

### Phase 5: Testing & Validation
13. Update `tests/conftest.py` with WebSocket test client setup and auth token generation

14. Add WebSocket integration tests in `tests/test_api.py` covering:
    - Authentication and connection establishment
    - Send message and receive response
    - Disconnect and verify history saved to DB
    - Reconnect and verify history retrieved and pre-loaded
    - Multi-turn conversation flow with context retention
    - Error handling (invalid token, connection drops, API errors)

## Design Decisions

### Session Model
- **Type**: Persistent per-user — each user has ONE chat history that persists across connections
- **Lifecycle**: 
  - Created on first connection (or retrieved if exists)
  - Updated on each disconnect (new messages appended)
  - History accumulates across multiple WebSocket sessions
- **History Pre-load**: All messages from user's single chat history loaded on connection; Gemini chat initialized with full context for true multi-turn capability

### Authentication
- **Method**: Auth token instead of URL path parameter
- **Rationale**: Cleaner URL, standard OAuth/JWT pattern, easier to revoke/refresh tokens
- **Implementation**: Extract `user_id` from token using existing security utilities; validate token on connect

### API Architecture
- **Endpoint**: `GET /ws/chatbot` (no user_id in path)
- **No REST Fallback**: WebSocket replaces the old `POST /chatbot/messages` endpoint entirely (separate implementation as user indicated)
- **Concurrent Connections**: Recommend enforcing 1 active session per user to prevent confusion; queue or reject excess connections

### Message Storage
- **Format**: JSON array in `messages` column
- **Rationale**: Flexibility; entire chat history captured atomically; one row per user simplifies queries
- **Unique Constraint**: One chat history row per user (prevents duplicates)

### AI Provider
- **Separation**: Gemini implementation is independent from old OpenAI implementation; no migration of existing data needed
- **Context**: Preserve mood/risk context building logic from current chatbot service

## Files to Modify/Create

| File | Action | Purpose |
|------|--------|---------|
| `app/models/chat_history.py` | Create | ChatHistory ORM model (one per user) |
| `app/crud/chat_history.py` | Create | ChatHistory CRUD operations |
| `alembic/versions/` | Create | Migration file for chat_history table |
| `app/services/chatbot_service.py` | Update | Gemini AI integration, chat session initialization |
| `app/api/chatbot.py` | Update | WebSocket endpoint, authentication, context building |
| `app/models/user.py` | Update | Add `chat_history` relationship |
| `app/config.py` | Update | Gemini API key configuration |
| `requirements.txt` | Update | Add `google-generativeai` |
| `tests/conftest.py` | Update | WebSocket test client setup |
| `tests/test_api.py` | Update | WebSocket integration tests |

## Verification Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Add Gemini API key to environment (`.env` or `export GEMINI_API_KEY=...`)
- [ ] Run Alembic migration: `alembic upgrade head`
- [ ] Verify `chat_history` table created in PostgreSQL with unique constraint on `user_id`
- [ ] Test WebSocket connection: Connect to `ws://localhost:8000/ws/chatbot` with valid auth token
- [ ] Test authentication: Verify invalid token rejected
- [ ] Test multi-turn messages: Send multiple messages, verify Gemini responses with context
- [ ] Test disconnect and history save: Verify messages accumulated in user's single chat_history row
- [ ] Test reconnect and history reload: Verify history pre-loaded into new connection
- [ ] Test persistence: Send messages in two separate WebSocket sessions, verify both sessions' messages in DB
- [ ] Run pytest: `pytest tests/test_api.py -v` (all WebSocket tests pass)
- [ ] Verify personality/mood context included in chat responses

## Further Considerations

### Rate Limiting
- **Current Decision**: Enforce 1 active session per user to prevent confusion
- **Alternative**: Allow concurrent sessions with queuing
- **Implementation**: Add connection counter per user; reject/queue excess connections

### Gemini API Limits
- **Issue**: Gemini has token limits per minute
- **Recommendation**: Add error handling for quota exceeded; document limits for users
- **Implementation**: Catch API errors, provide user-friendly messages, implement backoff logic

### Message History Archival/Cleanup
- **Current Decision**: Retain all historical messages indefinitely
- **Alternative**: Archive/prune after X days or if message count exceeds Y
- **Future Enhancement**: Add configurable archive policy if storage becomes an issue

### Connection Resilience
- **To Add**: Ping/pong mechanism to detect stale connections
- **To Add**: Graceful fallback if Gemini API is unavailable
- **To Add**: Reconnection window to resume same session if disconnected temporarily
