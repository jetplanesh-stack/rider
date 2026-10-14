# 🚴 Rider - Project Plan

## 📋 Project Overview
**rider** is an AI-powered tool to understand and learn about bicycle paths and cycling principles.

### One-line Summary
자전거도로의 이치 (Understanding the principles of bicycle paths)

### Why We're Building This
- Passion for cycling and bicycle infrastructure
- Need to make bicycle path knowledge accessible and interactive
- Leverage AI to provide intelligent guidance and information

---

## 🎯 Core Features

### Phase 1: Foundation
- [ ] AI-powered Q&A system for bicycle path knowledge
  - Use `ai_helper.py` to query Claude Haiku for cycling insights
  - Store and manage prompts related to cycling
  
- [ ] Basic documentation
  - Create knowledge base about bicycle paths
  - Document cycling principles and infrastructure

### Phase 2: Enhancement
- [ ] Interactive learning interface
  - Build UI for users to ask questions about cycling
  - Provide AI-generated explanations
  
- [ ] Knowledge management
  - Organize cycling information by category
  - Create reference guides

### Phase 3: Advanced Features
- [ ] Route planning assistance
  - Help users understand different cycling paths
  - Provide recommendations

- [ ] Community contributions
  - Allow users to share cycling path experiences
  - Build collaborative knowledge base

---

## 🌟 Expected Outcomes
- Users can accurately understand bicycle path principles
- Accessible knowledge about cycling infrastructure
- AI-assisted learning for cyclists
- Comprehensive cycling guidance platform

---

## 📁 Project Structure
```
rider/
├── ai_helper.py          # AI integration utility
├── PLAN.md              # This file
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (API keys)
└── [future modules]
```

---

## 🛠️ Technical Stack
- **Language**: Python
- **AI Provider**: Anthropic (Claude Haiku)
- **API Integration**: Anthropic Python client
- **Environment**: dotenv for configuration

---

## 📌 Next Steps
1. Clarify specific features and scope
2. Design user interface/interaction model
3. Build data models for cycling knowledge
4. Implement core AI-powered features
5. Add documentation and examples

---

## 🔗 Related Files
- `ai_helper.py` - AI utility module
- `.env` - Configuration file (not tracked)
- `requirements.txt` - Python dependencies

