pomodoro-timerflow/
├── .clinerules
├── .gitignore
├── Dockerfile
├── logo.png
├── README.md
├── restart_docker.sh
├── update_google_docs_code.py
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── alembic.ini
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── setup_db.py
│   │   ├── ws_manager.py
│   │   ├── alembic/
│   │   │   ├── env.py
│   │   │   ├── README
│   │   │   ├── script.py.mako
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── pomodoro.py
│   │   │   ├── tasks.py
├── pytest.ini
├── requirements.txt
├── static/
│   ├── app.js
│   ├── index.html
│   ├── styles.css
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_pomodoro.py
│   ├── test_tasks.py
├── data/
├── frontend-apps/
│   └── web-app/
│       ├── .gitignore
│       ├── package-lock.json
│       ├── package.json
│       ├── README.md
│       ├── public/
│       │   ├── favicon.ico
│       │   ├── index.html
│       │   ├── logo192.png
│       │   ├── logo512.png
│       │   ├── manifest.json
│       │   ├── robots.txt
│       ├── src/
│       │   ├── App.css
│       │   ├── App.js
│       │   ├── App.test.js
│       │   ├── index.css
│       │   ├── index.js
│       │   ├── logo.svg
│       │   ├── memory.js
│       │   ├── reportWebVitals.js
│       │   ├── setupTests.js
│       │   ├── components/
│       │   │   ├── LoginForm.js
│       │   │   ├── MainApp.js
│       │   │   ├── Settings.js
│       │   │   ├── TaskList.js
│       │   │   ├── Timer.js
│       │   ├── config/
│       │   │   ├── api.js
│       │   ├── hooks/
│       │   │   ├── useWebSocket.js
│       │   ├── styles/
│       │   │   ├── styles.js
│       │   │   ├── theme.css
├── logs/
│   └── error.log
├── prompts/
│   ├── prompt.md
│   ├── prompt.py