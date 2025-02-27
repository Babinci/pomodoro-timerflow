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

- **User Management**
  - Easy registration with email and username
  - Secure authentication
  - Account management including account deletion

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

## 🌐 Live Demo

You can access the live demo of the Pomodoro TimerFlow web application at:

[https://pomodoro.cypher-arena.com/](https://pomodoro.cypher-arena.com/)

To use the app:
- Register a new account with your email, username, and password
- Login with your credentials
- Create and manage tasks
- Set your preferred Pomodoro intervals
- Start tracking your work sessions

## 🏗️ Current State

- ✅ User registration and account management
- ✅ Functional backend server with API documentation
- ✅ Working web application with:
  - User authentication
  - Task management
  - Pomodoro timer
  - Real-time synchronization
- 🚧 Wear OS application (in development)
- ✅ Docker setup successful
- 📝 Current plans:
  - Create app for smartwatch wear os
  - Websockets server and client usage optimization
  - Add bell notification at end of round
  - Google authentication integration

## 🛠️ Getting Started

The backend server documentation will be available at `http://localhost:8003/docs`

you can build from dockerfile by:

 `docker build -t pomodoro-app .`

## 📱 Usage

1. Register a new account
2. Log in to the web application
3. Create and manage your tasks
4. Start tracking your Pomodoro sessions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note:** This project is under active development. Features and documentation will be updated regularly.