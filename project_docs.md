# Project Documentation

## Project Overview & Architecture

The Pomodoro TimerFlow is a cross-platform productivity tool designed to enhance focus and task management across web and smartwatch devices. It utilizes React Native for Web for the frontend, a FastAPI backend, WebSocket-based communication for real-time synchronization, and JWT authentication for secure user management.

The system architecture consists of the following components:

*   **Web Frontend:** A React Native for Web application that provides the user interface for managing tasks, setting timer intervals, and tracking progress.
*   **Backend Server:** A FastAPI application that handles user authentication, task management, and WebSocket communication.
*   **Wear OS App:** A React Native application that provides a simplified interface for starting and stopping the timer on a smartwatch.
*   **WebSocket Server:** A component of the backend server that manages real-time communication between the web frontend and the Wear OS app.
*   **Database:** A SQLite database that stores user data, tasks, and Pomodoro session history.

## Core Components Documentation

### Backend (FastAPI)

The backend is built using the FastAPI framework. Key components include:

*   `app/main.py`: The main application file that defines the API endpoints and initializes the database connection.
*   `app/auth.py`: Handles user authentication and authorization using JWT.
*   `app/database.py`: Defines the database models and manages database connections using SQLAlchemy.
*   `app/models.py`: Defines the database models for users, tasks, and Pomodoro sessions.
*   `app/schemas.py`: Defines the data schemas for API requests and responses.
*   `app/ws_manager.py`: Manages WebSocket connections and communication.

### Web Frontend (React Native for Web)

The web frontend is built using React Native for Web. Key components include:

*   `src/App.js`: The main application file that defines the application layout and routing.
*   `src/components/Timer.js`: Implements the Pomodoro timer logic and UI.
*   `src/components/TaskList.js`: Implements the task list and task management UI.
*   `src/components/LoginForm.js`: Implements the user login form.
*   `src/hooks/useWebSocket.js`: Manages WebSocket connections and communication with the backend.

### Wear OS App

The Wear OS app is a React Native application that provides a simplified interface for starting and stopping the timer on a smartwatch. The implementation is in progress.

### WebSocket Communication Protocol

The WebSocket communication protocol is used for real-time synchronization between the web frontend and the Wear OS app. The protocol defines the following message types:

*   `timer_start`: Starts the timer.
*   `timer_stop`: Stops the timer.
*   `timer_tick`: Sends the current timer value to the client.
*   `timer_complete`: Indicates that the timer has completed.

## Key Features & Implementation Details

### User Authentication and Account Management

User authentication and account management are implemented using JWT. The backend provides API endpoints for user registration, login, and account management.

### Timer Functionality and State Management

The timer functionality is implemented in the web frontend using React Native's `useState` hook. The timer state is managed using a WebSocket connection to the backend.

### Task Tracking and Pomodoro Session Management

Task tracking and Pomodoro session management are implemented using the backend's API endpoints. The backend stores task data and Pomodoro session history in the SQLite database.

### Real-Time Synchronization Between Devices

Real-time synchronization between devices is implemented using WebSocket communication. The backend sends timer updates to all connected clients in real-time.

### Settings Customization (Short/Long Presets)

Settings customization is implemented in the web frontend using React Native's `useState` hook. The user can customize the short and long Pomodoro intervals.

## Project Status & Roadmap

### Working Features and Components

*   User registration and account management
*   Functional backend server with API documentation
*   Working web application with:
    *   User authentication
    *   Task management
    *   Pomodoro timer
    *   Real-time synchronization
*   Docker setup successful

### Known Issues and Bugs

*   Timer problems:
    *   After a long round, there is a short break - it should be a break from the long preset, and the user can't change the break to long.
    *   After 1 round and 1 break, the user sees a "start break" button instead of "start".
    *   When working in a round and clicking pause, the user can't resume - the screen "freezes".
    *   It is very hard to change to long intervals.
    *   After 25 short work sessions, the user sees a 10 min short break (it should be 5 min as short in settings) - and can't change during the break to a short break.
    *   When the user clicks a new browser tab, it resets to that new one - the first was counting 49, and then the user opened a new tab, and it was 25 in the second and reset.
    *   The timer should work even if the user closes the browser, so it should have a universal source in the websockets backend server, and so the timer should go to break/end of break and have a state. The only thing is that maybe each 5 AM local time, it should reset as for a new date (with some clever resources management in the timer algorithm).
*   Bugs:
    *   Failed to update task: Failed to update task with increasing number of pomodoros
    *   Server disconnecting problem

### Planned Improvements and Future Development

*   Timers tests
*   Wear OS app development (implementation in progress)
*   Description field with more options for text formatting like tabs and bold font
*   Websockets server and client usage optimization
*   Problems with pause time - after long work, the user can see a short break and can't change to long
*   Mess with timer
*   After a finished session, the user can't see it in the counter number
*   Confetti after a finished task
*   Optional bell ring at the end of the round
*   Google auth

### Current Focus

The current focus is on Wear OS app development.

## Code Organization

```
.gitignore
.rooignore
Dockerfile
README.md
backend/
    app/
        __init__.py
        alembic.ini
        alembic/
            README
            env.py
            script.py.mako
        auth.py
        database.py
        main.py
        models.py
        routers/
            __init__.py
            auth.py
            pomodoro_websocket.py
            tasks.py
            users.py
        schemas.py
        setup_db.py
        ws_manager.py
    pytest.ini
    requirements.txt
    static/
        app.js
        index.html
        styles.css
    tests/
        __init__.py
        conftest.py
        test_auth.py
        test_pomodoro.py
        test_tasks.py
bin/
diff.md
frontend-apps/
    wear-app/
        PomodoroWear/
            .bundle/
                config
            .eslintrc.js
            .gitignore
            .prettierrc.js
            .vscode/
                launch.json
            .watchmanconfig
            App.js
            App.tsx
            Gemfile
            README.md
            __tests__/
                App.test.tsx
            android/
                app/
                    build.gradle
                    debug.keystore
                    proguard-rules.pro
                    src/
                        debug/
                            AndroidManifest.xml
                        main/
                            AndroidManifest.xml
                            java/
                                com/
                                    pomodorowear/
                                        MainActivity.kt
                                        MainApplication.kt
                            res/
                                drawable/
                                    rn_edit_text_material.xml
                                mipmap-hdpi/
                                    ic_launcher.png
                                    ic_launcher_round.png
                                mipmap-mdpi/
                                    ic_launcher.png
                                    ic_launcher_round.png
                                mipmap-xhdpi/
                                    ic_launcher.png
                                    ic_launcher_round.png
                                mipmap-xxhdpi/
                                    ic_launcher.png
                                    ic_launcher_round.png
                                mipmap-xxxhdpi/
                                    ic_launcher.png
                                    ic_launcher_round.png
                                values/
                                    strings.xml
                                    styles.xml
                build.gradle
                gradle.properties
                gradle/
                    wrapper/
                        gradle-wrapper.jar
                        gradle-wrapper.properties
                gradlew
                gradlew.bat
                local.properties
                settings.gradle
            app.json
            babel.config.js
            index.js
            ios/
                .xcode.env
                Podfile
                PomodoroWear.xcodeproj/
                    project.pbxproj
                    xcshareddata/
                        xcschemes/
                            PomodoroWear.xcscheme
                PomodoroWear/
                    AppDelegate.swift
                    Images.xcassets/
                        AppIcon.appiconset/
                            Contents.json
                        Contents.json
                    Info.plist
                    LaunchScreen.storyboard
                    PrivacyInfo.xcprivacy
            jest.config.js
            metro.config.js
            package-lock.json
            package.json
            src/
                config/
                    api.js
                context/
                    TimerContext.js
                hooks/
                    useWebSocket.js
                screens/
                    ControlsScreen.js
                    LoginScreen.js
                    TaskDescriptionScreen.js
                    TimerScreen.js
                services/
                    wearConnectivity.js
            tsconfig.json
    web-app/
        .gitignore
        README.md
        package-lock.json
        package.json
        public/
            favicon.ico
            favicon.png
            index.html
            logo192.png
            logo512.png
            manifest.json
            robots.txt
        src/
            App.css
            App.js
            App.test.js
            assets/
                bell.mp3
            components/
                LoginForm.js
                MainApp.js
                Settings.js
                TaskList.js
                Timer.js
                UserProfile.js
            config/
                api.js
            hooks/
                useWebSocket.js
            index.css
            index.js
            logo.svg
            memory.js
            reportWebVitals.js
            setupTests.js
            styles/
                styles.js
            theme.css
implementation_plans/
    checkpoints_plan.md
    implement_wear_os.md
logo.png
memory-bank/
    activeContext.md
    productContext.md
    progress.md
    projectbrief.md
    systemPatterns.md
    techContext.md
    wear_os_app_requirements.md
    wear_os_status.md
    websocket_timer_logic.md
restart_docker.sh

## Development & Deployment

The backend server documentation will be available at `http://localhost:8003/docs`

You can build from dockerfile by:

`docker build -t pomodoro-app .`
