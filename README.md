# Symbiote Learning App v2.0

**AI-Powered Collaborative Learning Platform with Clean Architecture**

An innovative learning system that combines multiple AI agents with proven pedagogical principles to create personalized, engaging learning experiences.

## ✨ Key Features

###  Multi-Agent System
Four specialized AI agents collaborate to enhance learning:
- **Socratic Tutor**: Guides through thought-provoking questions
- **Virtual Peer**: Collaborates and makes intentional mistakes
- **Provocateur**: Challenges with games and real-world scenarios
- **Teachable Agent**: Learns from the user to reinforce understanding

###  Adaptive Learning Paths
- Three progressive phases: Exploration → Construction → Creation
- Personalized based on user profile and performance
- Real-time adaptation to learning style

###  Gamification System
- Dynamic point system with action multipliers
- Real-time level progression
- Hint system with strategic penalties
- Achievement tracking

###  Analytics & Insights
- Performance tracking by topic
- Weak area identification
- Personalized recommendations
- Learning history management

###  Clean Architecture
- Modular, extensible design
- Clear separation of concerns
- Easy to test and maintain
- SOLID principles throughout

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry
- OpenAI API key

### Installation

1. **Clone and setup**:
```bash
cd symbiote_learning_app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run**:
```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend
streamlit run streamlit_app.py
```

4. **Access**:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## 📁 Project Structure

```
src/
├── core/              # Abstractions and interfaces
├── schemas/           # Data models (Pydantic)
├── agents/            # Multi-agent system
├── services/          # Business logic
├── api/               # REST API routes
└── ui/                # UI components
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## 🎓 How It Works

### User Journey

1. **Welcome**: Introduction to the platform
2. **Profile**: Create learning profile (name, age, subject, purpose)
3. **Learning**: Interactive chat with AI agents
4. **Progress**: Track points, level, and performance

### Learning Flow

```
User Input
    ↓
Orchestrator selects agent
    ↓
Agent processes input with context
    ↓
Points awarded/deducted
    ↓
History updated
    ↓
Response displayed
```

## 🤖 Agent System

### Socratic Tutor
- Asks thought-provoking questions
- Manages learning path
- Decides when to involve other agents

### Virtual Peer
- Collaborates on tasks
- Makes intentional (30%) mistakes
- Provides encouragement

### Provocateur
- Creates engaging challenges
- Presents real-world scenarios
- Maintains interest with humor

### Teachable Agent
- Evaluates user explanations
- Identifies knowledge gaps
- Awards bonus points for teaching

## 🎮 Gamification

### Points System
| Action | Multiplier | Example |
|--------|-----------|---------|
| Curiosity | 1.5x | 10 pts → 15 pts |
| Critical Thinking | 2.0x | 10 pts → 20 pts |
| Collaboration | 1.3x | 10 pts → 13 pts |
| Teaching | 2.5x | 20 pts → 50 pts |
| Challenge | 3.0x | 20 pts → 60 pts |

### Levels
- Level = (Total Points ÷ 100) + 1
- Progress bar shows advancement
- Recommendations update per level

## 📚 API Endpoints

### Sessions
- `POST /api/v1/sessions/create` - Create session
- `GET /api/v1/sessions/{session_id}` - Get session info
- `DELETE /api/v1/sessions/{session_id}` - Close session

### Chat
- `POST /api/v1/chat/message` - Send message
- `POST /api/v1/chat/hint` - Request hint

### Analytics
- `GET /api/v1/analytics/points/{session_id}` - Get points
- `GET /api/v1/analytics/history/{session_id}` - Get history
- `GET /api/v1/analytics/performance/{session_id}` - Get performance



## 🙏 Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- Streamlit - Rapid UI development
- Pydantic - Data validation
- OpenAI API - LLM integration


## 🎯 Learning Outcomes

Users will:
1. Develop critical thinking through Socratic questioning
2. Learn collaboratively with AI peers
3. Apply knowledge through project-based learning
4. Receive personalized feedback
5. Maintain engagement through gamification
6. Track progress with real-time analytics
7. Identify and improve weak areas

