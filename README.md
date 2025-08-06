# AI Manager

**Empowering Music Artists and Professionals with Robust AI-Driven Knowledge & Strategy**

---

## 🚀 Vision & Goals

- **Personal Manager Persona:** Provide each user with an AI assistant that blends personal knowledge (uploaded docs, notes, history) and global industry intelligence for world-class advice.
- **Robust, Scalable RAG:** Use the latest retrieval-augmented generation (RAG) techniques for context-aware, accurate, and explainable answers.
- **Hybrid Semantic Search:** Maximize recall and relevance by combining multiple embedding models and knowledge bases.
- **Privacy & Security:** Strictly isolate personal data and audit all knowledge access.
- **Observability:** Maintain full traceability and logging for all retrieval and reasoning steps.

---

## 🧠 System Overview

### Core Components
- **Backend (Python):** Orchestrates ingestion, semantic search, intent classification, context retrieval, and LLM prompt construction.
- **Frontend (Streamlit):** Modern, responsive UI for document upload, chat, and analytics.
- **Qdrant Vector DB:** Stores all chunked knowledge with embeddings from multiple models.
- **OpenAI API:** Provides embeddings and LLM completions.

---

## 🔎 Hybrid Retriever: How & Why

### **Knowledge Bases (KBs):**
- **Personal KB:** User-specific docs, only accessible by that user (filtered by `user_id`).
- **Global KB:** Industry-wide docs, best practices, and general info (never filtered by `user_id`).

### **Hybrid Multi-Embedding Search:**
- For every query, generate embeddings using:
  - OpenAI (`text-embedding-3-small`)
  - BGE (`bge-base-en-v1.5`)
  - B2M5
- Query Qdrant for each embedding across all relevant KBs.
- Merge and deduplicate results by chunk.

### **KB Targeting Logic:**
| Query Intent | KBs Targeted         | Filtered by user_id? | Why?                                 |
|--------------|---------------------|----------------------|--------------------------------------|
| personal     | personal, global    | personal only        | Personalization + industry context   |
| global       | global              | never                | Industry context only                |
| hybrid       | personal, global    | personal only        | Both personal and industry blended   |

- **Personal KB**: Only if query is personal/hybrid **and** user is authenticated.
- **Global KB**: Always targeted for every query.

---

## 🛠️ System Workflow (Mermaid Diagram)

```mermaid
flowchart TD
    A[User Query] --> B{Intent Classification}\n(LLM + fallback)
    B -->|personal| C1[Embed Query (all models)]
    B -->|global| C2[Embed Query (all models)]
    B -->|hybrid| C3[Embed Query (all models)]
    C1 --> D1[Search Personal KB (all models)\nfilter by user_id]
    C1 --> D2[Search Global KB (all models)]
    C2 --> D3[Search Global KB (all models)]
    C3 --> D4[Search Personal KB (all models)\nfilter by user_id]
    C3 --> D5[Search Global KB (all models)]
    D1 & D2 --> E1[Merge + Deduplicate]
    D3 --> E2[Deduplicate]
    D4 & D5 --> E3[Merge + Deduplicate]
    E1 & E2 & E3 --> G[Build Prompt]
    G --> H[LLM Completion]
    H --> I[Response]
```

---

## 🧩 Implementation Details

### Ingestion
- Chunk documents using token overlap.
- Generate and store embeddings for all supported models.
- Store in Qdrant with appropriate KB and user_id.

### Retrieval
- Classify query intent (LLM-based, fallback to keywords).
- For each embedding model, search all relevant KBs.
- Merge/deduplicate results.
- Build prompt with clear context source separation.

### Security & Privacy
- Personal KBs are always filtered by user_id.
- Global KBs are never filtered by user_id.
- All access and retrievals are logged.
- No sensitive data in logs.

### Logging & Observability
- Structured logs to `logs/ai_manager.log` (see `logging.conf`).
- All major retrieval, classification, and LLM steps logged.
- Errors and fallbacks are traceable.

### Deployment & Setup
- Requires Python 3.10+, Docker, and Docker Compose.
- Environment variables:
  - `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION`
- Start with: `docker-compose up --build`
- Frontend at `localhost:8501`, backend at `localhost:8000`

### Test Cases & Quality
- Test classification, retrieval, and ingestion.
- Example:
  - `test_classify_intent`: Ensures correct intent detection.
  - `test_retrieve_context`: Ensures correct KB targeting and context retrieval.
  - `test_prompt_building`: Ensures context is separated and prompt is well-formed.
- Use Django test runner: `docker-compose exec backend python manage.py test`

---

## 🏆 Alignment with Vision
- **Personalization:** Each user gets tailored, private, and industry-aware answers.
- **Robustness:** Hybrid search ensures no relevant context is missed.
- **Transparency:** All KB targeting and context selection is explainable and logged.
- **Scalability:** Modular, multi-KB, multi-embedding design supports future growth.
- **Maintainability:** All logic and workflows are documented and testable.

---

## 📚 Onboarding Checklist
- Clone repo, set up `.env` with required keys.
- Ingest your documents (re-ingest if upgrading to hybrid search).
- Start all services with Docker Compose.
- Use the chat and analytics dashboard.
- Review logs for troubleshooting.

---

For further details, see code comments and logging output. For any questions, open an issue or contact the maintainer.


## 🎯 Project Vision

**AI Manager** is a comprehensive AI-powered system designed specifically for music artists to revolutionize their career development and creative process. The system combines advanced AI capabilities with personalized knowledge management to provide strategic guidance, creative insights, and business intelligence tailored to each artist's unique journey.

### Core Mission
Transform how music artists approach their careers by providing:
- **Intelligent Document Analysis**: AI-powered insights from personal and industry documents
- **Strategic Career Guidance**: Data-driven recommendations for career development
- **Creative Process Enhancement**: AI-assisted creative decision making
- **Business Intelligence**: Market analysis and opportunity identification
- **Personalized Learning**: Context-aware advice based on individual artist profiles

## 🛠 Tech Stack

### Backend Architecture
- **Framework**: Django 5.2.4 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT with Django REST Framework Simple JWT
- **API**: RESTful API with comprehensive endpoints
- **CORS**: django-cors-headers for cross-origin requests

### AI & Machine Learning
- **LLM**: OpenAI GPT-3.5-turbo for intelligent responses
- **Vector Database**: Qdrant for semantic search and RAG
- **Embeddings**: OpenAI text-embedding-3-small for document processing
- **RAG Pipeline**: Retrieval-Augmented Generation for context-aware responses
- **Document Processing**: PyPDF2, python-docx for multi-format support

### Frontend
- **Framework**: Streamlit for rapid web application development
- **UI/UX**: Custom black and red theme with modern design
- **State Management**: Streamlit session state for user data
- **Real-time Updates**: Streamlit's reactive framework

### Infrastructure
- **Containerization**: Docker with multi-service orchestration
- **Development**: Docker Compose for local development
- **Vector Database**: Qdrant container for semantic search
- **Environment Management**: Python-dotenv for configuration

## 🚀 Comprehensive Setup & Run Instructions

### Prerequisites

#### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **Internet**: Stable connection for Docker images and OpenAI API

#### Required Software
1. **Docker Desktop** (Windows/macOS) or **Docker Engine** (Linux)
   - Download from: https://www.docker.com/products/docker-desktop
   - Ensure Docker Compose is included (usually comes with Docker Desktop)
   - Verify installation: `docker --version` and `docker-compose --version`

2. **Git** (for cloning repository)
   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

3. **OpenAI API Key**
   - Sign up at: https://platform.openai.com/
   - Create API key in your account settings
   - Note: Free tier includes $5 credit, paid plans available

### Complete Setup Process

#### Step 1: Repository Setup
```bash
# Clone the repository
git clone <repository-url>
cd sse-aiManager

# Verify project structure
ls -la
# Should show: backend/, st_frontend/, docker-compose.yml, README.md
```

#### Step 2: Environment Configuration
```bash
# Create environment file from template
cp backend/.env.example backend/.env

# Edit the environment file with your settings
# On Windows: notepad backend/.env
# On macOS/Linux: nano backend/.env or vim backend/.env

# Required environment variables to set:
# OPENAI_API_KEY=your-actual-openai-api-key-here
# DJANGO_SECRET_KEY=your-secret-key-here (or leave default for development)
# DEBUG=True (for development)
```

#### Step 3: Docker Setup
```bash
# Build and start all services
docker-compose up -d

# Verify all services are running
docker-compose ps

# Expected output:
# Name                    Command               State           Ports
# -----------------------------------------------------------------------------
# sse-aimanager_backend_1   python manage.py runserver 0.0.0.0:8000   Up      0.0.0.0:8000->8000/tcp
# sse-aimanager_frontend_1  streamlit run main.py --server.port 8501   Up      0.0.0.0:8501->8501/tcp
# sse-aimanager_qdrant_1    ./qdrant                              Up      0.0.0.0:6333->6333/tcp
```

#### Step 4: Database Initialization
```bash
# Run database migrations
docker-compose exec backend python manage.py migrate

# Create a superuser (optional, for admin access)
docker-compose exec backend python manage.py createsuperuser
# Follow prompts to create admin account

# Verify database setup
docker-compose exec backend python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.count()
>>> exit()
```

#### Step 5: Service Verification
```bash
# Check backend API health
curl http://localhost:8000/api/health/ || echo "Backend not ready yet"

# Check Qdrant vector database
curl http://localhost:6333/collections || echo "Qdrant not ready yet"

# Check frontend accessibility
curl -I http://localhost:8501 || echo "Frontend not ready yet"
```

### Accessing the Application

#### Web Interface
- **Main Application**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Qdrant Dashboard**: http://localhost:6333
- **Django Admin**: http://localhost:8000/admin (if superuser created)

#### First-Time Setup
1. **Open browser** and navigate to http://localhost:8501
2. **Register account** with your email and password
3. **Complete profile** with artist information
4. **Upload first document** to test the system
5. **Start AI conversation** to verify functionality

### Alternative Setup Methods

#### Local Development (Without Docker)
```bash
# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Qdrant Setup (separate terminal)
docker run -p 6333:6333 qdrant/qdrant

# Frontend Setup (separate terminal)
cd st_frontend
pip install streamlit requests python-dotenv
streamlit run main.py --server.port 8501
```

#### Production Deployment
```bash
# Set production environment
export DJANGO_SETTINGS_MODULE=manager_backend.settings_production
export DEBUG=False
export ALLOWED_HOSTS=your-domain.com

# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production settings
docker-compose -f docker-compose.prod.yml up -d
```

### Troubleshooting Setup Issues

#### Common Problems & Solutions

**1. Docker Not Starting**
```bash
# Check Docker service
docker info

# Restart Docker Desktop/Engine
# Windows/macOS: Restart Docker Desktop
# Linux: sudo systemctl restart docker

# Verify Docker Compose
docker-compose --version
```

**2. Port Conflicts**
```bash
# Check if ports are in use
netstat -an | grep 8501  # Frontend port
netstat -an | grep 8000  # Backend port
netstat -an | grep 6333  # Qdrant port

# Kill processes using these ports (if needed)
# Windows: netstat -ano | findstr :8501
# Linux/macOS: lsof -i :8501
```

**3. OpenAI API Issues**
```bash
# Test API key
curl -H "Authorization: Bearer YOUR_OPENAI_KEY" \
  https://api.openai.com/v1/models

# Check environment variable
docker-compose exec backend python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

**4. Database Issues**
```bash
# Reset database (WARNING: Deletes all data)
docker-compose down
docker volume rm sse-aimanager_backend_data
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

**5. Memory Issues**
```bash
# Check Docker resource usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Recommended: 4GB+ for smooth operation
```

### Development Commands

#### Daily Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up --build -d
```

#### Database Management
```bash
# Access Django shell
docker-compose exec backend python manage.py shell

# Create new migration
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Reset database
docker-compose exec backend python manage.py flush
```

#### Testing
```bash
# Run tests
docker-compose exec backend python manage.py test

# Check API endpoints
curl http://localhost:8000/api/health/

# Test AI functionality
curl -X POST http://localhost:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"conversation":1,"text":"Hello, how are you?"}'
```

### Performance Optimization

#### Resource Allocation
```bash
# Monitor resource usage
docker stats

# Optimize Docker settings:
# - Memory: 4GB+ recommended
# - CPU: 2+ cores recommended
# - Disk: SSD preferred for better performance
```

#### Scaling for Production
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Set up reverse proxy (nginx)
# Configure SSL certificates
# Set up monitoring and logging
# Implement backup strategies
```

## 👥 Detailed User Workflows

### 🎤 Independent Artists

#### Workflow: Career Development & Strategy
1. **Account Setup**
   - Register with artist email and create profile
   - Complete artist bio, genre, and career stage information
   - Set career goals and target audience

2. **Document Upload & Analysis**
   - Upload press kits, bios, and promotional materials
   - Add industry research documents and competitor analysis
   - Upload previous releases and performance data
   - System automatically processes and indexes documents

3. **AI-Powered Career Planning**
   - Start AI chat conversation: "Help me plan my next release strategy"
   - AI analyzes your documents and provides personalized advice
   - Get recommendations for marketing, audience targeting, and release timing
   - Discuss creative direction and industry positioning

4. **Strategic Implementation**
   - Use AI consultancy for detailed action plans
   - Get step-by-step guidance for career milestones
   - Track progress and adjust strategies based on AI insights
   - Export recommendations for team collaboration

#### Use Cases:
- **Release Planning**: "How should I approach my next album release?"
- **Marketing Strategy**: "What marketing channels work best for my genre?"
- **Audience Development**: "How can I grow my fanbase effectively?"
- **Industry Networking**: "What industry events should I attend?"

### 🎧 Music Producers

#### Workflow: Creative Process & Market Analysis
1. **Portfolio Documentation**
   - Upload production credits and discography
   - Add technical specifications and equipment lists
   - Include client testimonials and project outcomes
   - Document production techniques and workflows

2. **Market Intelligence**
   - Upload industry reports and trend analysis
   - Add competitor producer research
   - Include genre-specific market data
   - Track successful production patterns

3. **Creative Decision Support**
   - AI chat: "What production trends are emerging in my genre?"
   - Get insights on current market demands
   - Analyze successful production techniques
   - Receive recommendations for equipment and software

4. **Business Development**
   - Use AI to identify potential clients and opportunities
   - Get pricing strategy recommendations
   - Develop marketing materials and proposals
   - Track industry trends and adapt services

#### Use Cases:
- **Trend Analysis**: "What production styles are trending in hip-hop?"
- **Equipment Decisions**: "Should I invest in new studio equipment?"
- **Client Targeting**: "What types of artists should I approach?"
- **Pricing Strategy**: "How should I price my production services?"

### ✍️ Songwriters

#### Workflow: Creative Inspiration & Industry Knowledge
1. **Creative Portfolio**
   - Upload lyrics, song structures, and writing samples
   - Document writing processes and inspiration sources
   - Add collaboration history and co-writing credits
   - Include feedback and performance data

2. **Industry Knowledge Base**
   - Upload publishing contracts and royalty information
   - Add industry contact lists and networking notes
   - Include songwriting competition and opportunity data
   - Document successful song placement strategies

3. **Creative Enhancement**
   - AI chat: "Help me develop this song concept further"
   - Get lyrical suggestions and structural advice
   - Receive feedback on commercial viability
   - Explore different genre adaptations

4. **Career Advancement**
   - Identify publishing opportunities and sync licensing
   - Get recommendations for collaboration partners
   - Develop pitching strategies for different markets
   - Track song performance and royalty optimization

#### Use Cases:
- **Lyric Development**: "How can I improve this chorus?"
- **Genre Adaptation**: "How would this song work in country music?"
- **Publishing Strategy**: "What publishers should I approach?"
- **Collaboration**: "Who would be good co-writers for this project?"

### 🎯 Music Managers

#### Workflow: Artist Development & Business Strategy
1. **Artist Portfolio Management**
   - Upload comprehensive artist profiles and career histories
   - Document performance data and audience analytics
   - Include financial records and revenue streams
   - Add industry relationships and contact networks

2. **Strategic Planning**
   - AI chat: "Create a 12-month development plan for my artist"
   - Get data-driven recommendations for career milestones
   - Analyze market opportunities and competitive landscape
   - Develop comprehensive business strategies

3. **Resource Optimization**
   - Identify best investment opportunities for artist development
   - Get recommendations for team building and partnerships
   - Optimize marketing budgets and campaign strategies
   - Track ROI and performance metrics

4. **Industry Intelligence**
   - Monitor industry trends and market changes
   - Identify new opportunities and emerging platforms
   - Develop networking strategies and relationship building
   - Stay ahead of industry disruptions and innovations

#### Use Cases:
- **Artist Development**: "What's the best path for my artist's career?"
- **Revenue Optimization**: "How can I maximize my artist's income?"
- **Team Building**: "What team members should I hire next?"
- **Market Analysis**: "What opportunities exist in emerging markets?"

- **Global Knowledgebase**: Access industry-wide information
- **Document Types**: Support for TXT, PDF, and DOCX files
- **Semantic Search**: AI-powered search through your documents
- **Automatic Processing**: Documents are chunked and embedded for AI analysis

### 💬 AI Chat System
- **Conversation Management**: Create and manage multiple chat sessions
- **Context-Aware**: AI remembers conversation history
- **Personalized Responses**: Based on your knowledgebase
- **Real-time Interaction**: Instant AI responses

### 💡 AI Consultancy
- **Strategic Recommendations**: Personalized career advice
- **Data Analysis**: Insights from your uploaded documents
- **Action Planning**: Step-by-step guidance for your music career
- **Progress Tracking**: Monitor your growth over time

### 📊 Dashboard Analytics
- **Activity Overview**: Track your usage and engagement
- **Quick Actions**: Easy access to key features
- **Recent Activity**: Monitor your latest actions
- **System Status**: Check backend connectivity

## 🐛 Debugging Guide

### Common Issues and Solutions

#### 1. AI Not Responding
```bash
# Check OpenAI API key
docker-compose exec backend python manage.py shell
>>> import os
>>> print(os.getenv('OPENAI_API_KEY'))

# Check API connectivity
curl -H "Authorization: Bearer YOUR_OPENAI_KEY" \
  https://api.openai.com/v1/models
```

#### 2. Qdrant Connection Issues
```bash
# Check Qdrant service
docker-compose logs qdrant

# Test Qdrant connectivity
curl http://localhost:6333/collections
```

#### 3. Document Upload Failures
```bash
# Check file permissions
docker-compose exec backend ls -la /app/media

# Verify document processing
docker-compose logs backend | grep "ingestion"
```

#### 4. Frontend Not Loading
```bash
# Check Streamlit service
docker-compose logs frontend

# Verify port availability
netstat -an | grep 8501
```

### Log Analysis
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f qdrant

# Check for errors
docker-compose logs | grep -i error
```

## 🎯 Goal Alignment

### Primary Objectives Met

#### 1. **AI-Powered Career Development** ✅
- **RAG Implementation**: AI uses personal and global knowledgebase
- **Context-Aware Responses**: Personalized advice based on artist's data
- **Strategic Guidance**: Career planning and business intelligence

#### 2. **Knowledge Management** ✅
- **Dual Knowledgebase**: Personal and global document management
- **Semantic Search**: AI-powered document discovery
- **Multi-format Support**: TXT, PDF, DOCX processing

#### 3. **User Experience** ✅
- **Modern UI/UX**: Professional black and red theme
- **Responsive Design**: Works on all devices
- **Intuitive Navigation**: Clear user journey

#### 4. **Scalability** ✅
- **Modular Architecture**: Separate services for different functions
- **Containerization**: Docker-based deployment
- **Database Flexibility**: SQLite/PostgreSQL support

### Success Metrics

#### Technical Metrics
- **Response Time**: AI responses under 3 seconds
- **Uptime**: 99.9% service availability
- **Accuracy**: Context-relevant AI responses
- **Scalability**: Support for 1000+ concurrent users

#### User Experience Metrics
- **Onboarding Time**: New user setup under 5 minutes
- **Feature Adoption**: 80%+ users engage with AI chat
- **Document Upload**: 90%+ successful processing rate
- **User Retention**: 70%+ weekly active users

#### Business Impact Metrics
- **Career Insights**: 85%+ users report valuable insights
- **Strategic Decisions**: 60%+ users implement AI recommendations
- **Time Savings**: 50%+ reduction in research time
- **Knowledge Utilization**: 75%+ of uploaded documents referenced

---

**AI Manager** - Empowering Music Artists with AI-Driven Intelligence 