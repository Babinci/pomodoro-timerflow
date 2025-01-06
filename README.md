# Pomodoro TimerFlow

<div align="center">
  <img src="logo.png" alt="Pomodoro TimerFlow Logo" width="400">
</div>

A cross-platform productivity system that helps you maintain focus and track tasks across web, mobile, and smartwatch devices.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Overview

Pomodoro TimerFlow is a comprehensive productivity tool that lets you:
- Set up and manage tasks through web/mobile interfaces
- Track your Pomodoro sessions on your smartwatch
- Maintain seamless synchronization across all your devices
- Customize Pomodoro intervals to match your work style

## 🚀 Features

- **Cross-Platform Support**
  - Web application
  - Mobile app (planned)
  - Wear OS smartwatch integration (in development)

- **Real-Time Synchronization**
  - Instant updates across all connected devices
  - WebSocket-based communication
  - Robust state management

- **Task Management**
  - Create and organize tasks
  - Track Pomodoro sessions per task
  - Add descriptions and estimates
  - Monitor progress

## 💻 Tech Stack

### Backend
- FastAPI framework
- SQLAlchemy ORM
- WebSocket support
- JWT authentication
- SQLite database

### Frontend
- React Native for Web
- Shared codebase for web/mobile/watch
- Real-time WebSocket integration
- Responsive design

## 🏗️ Current State

- ✅ Functional backend server with API documentation
- ✅ Working web application with:
  - User authentication
  - Task management
  - Pomodoro timer
  - Real-time synchronization
- 🚧 Wear OS application (in development)

## 📋 Roadmap

1. **Phase 1 (Current)**
   - Deploy web app and backend to production hosting
   - Implement proper registration and login flow

2. **Phase 2**
   - Refine Wear OS application
   - Add offline support
   - Enhance synchronization

3. **Phase 3**
   - Mobile app development
   - Cross-platform testing
   - Performance optimization

## 🛠️ Getting Started

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Web App Setup**
   ```bash
   cd frontend-apps/web-app
   npm install
   npm start
   ```

The backend server documentation will be available at `http://localhost:8000/docs`

## 📱 Usage

1. Register using the backend server documentation
2. Log in to the web application
3. Create and manage your tasks
4. Start tracking your Pomodoro sessions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note:** This project is under active development. Features and documentation will be updated regularly.