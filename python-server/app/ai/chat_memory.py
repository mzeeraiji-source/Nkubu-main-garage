"""
Chat Memory - Conversation history with vector embeddings
Stores and retrieves conversation context for AI assistant
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """Represents a chat message"""
    id: str
    session_id: str
    user_id: str
    role: str  # user, assistant
    content: str
    embedding: Optional[List[float]] = None
    timestamp: datetime = None


class ChatMemory:
    """Manages conversation history and context"""

    def __init__(self, max_history: int = 20, retention_days: int = 30):
        """Initialize chat memory"""
        self.max_history = max_history
        self.retention_days = retention_days
        self.conversations = {}  # In-memory store, replace with DB
        logger.info(f"ChatMemory initialized: max_history={max_history}")

    def add_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: str,
    ) -> ChatMessage:
        """Add a message to conversation history"""
        message = ChatMessage(
            id=f"msg_{int(datetime.now().timestamp())}",
            session_id=session_id,
            user_id=user_id,
            role=role,
            content=content,
            timestamp=datetime.now(),
        )

        if session_id not in self.conversations:
            self.conversations[session_id] = []

        self.conversations[session_id].append(message)

        # Keep only recent messages
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history:]

        logger.debug(f"Message added to session {session_id}")
        return message

    def get_conversation_history(
        self,
        session_id: str,
        limit: int = None,
    ) -> List[ChatMessage]:
        """Retrieve conversation history for a session"""
        history = self.conversations.get(session_id, [])
        if limit:
            history = history[-limit:]
        return history

    def get_recent_context(
        self,
        session_id: str,
        num_messages: int = 5,
    ) -> List[Dict]:
        """Get recent conversation context formatted for Claude"""
        history = self.get_conversation_history(session_id, limit=num_messages)
        return [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in history
        ]

    def clear_session(
        self,
        session_id: str,
    ) -> bool:
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
            logger.info(f"Session {session_id} cleared")
            return True
        return False

    def cleanup_old_conversations(
        self,
        retention_days: Optional[int] = None,
    ) -> int:
        """Remove old conversations beyond retention period"""
        days = retention_days or self.retention_days
        cutoff_date = datetime.now() - timedelta(days=days)

        removed_count = 0
        sessions_to_remove = []

        for session_id, messages in self.conversations.items():
            if messages and messages[-1].timestamp < cutoff_date:
                sessions_to_remove.append(session_id)
                removed_count += 1

        for session_id in sessions_to_remove:
            del self.conversations[session_id]

        logger.info(f"Cleaned up {removed_count} old conversation sessions")
        return removed_count
