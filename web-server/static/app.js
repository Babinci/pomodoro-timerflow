let token = localStorage.getItem('token');
let currentTask = null;
let timerInterval = null;
let timeLeft = 25 * 60;
let isRunning = false;
let sessionType = 'work';
let currentSessionNumber = 1;
let ws = null;

// Show/hide main app based on stored token
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('mainApp').classList.remove('hidden');
        initializeWebSocket();
        loadTasks();
    }
});

async function login() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    // Validate input fields
    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch('/token', {
            method: 'POST',
            body: formData
        });

        // Handle non-200 responses explicitly
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed');
        }

        const data = await response.json();
        
        // Validate that we received a token
        if (!data.access_token) {
            throw new Error('No access token received');
        }

        // Store token and user info
        token = data.access_token;
        localStorage.setItem('token', token);
        
        // Show main app
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('mainApp').classList.remove('hidden');
        
        // Initialize app
        initializeWebSocket();
        loadTasks();
    } catch (error) {
        alert(error.message);
        // Clear any stored credentials on error
        localStorage.removeItem('token');
    }
}

// Check login state on page load
document.addEventListener('DOMContentLoaded', () => {
    const storedToken = localStorage.getItem('token');
    
    if (storedToken) {
        // Verify token is still valid
        fetch('/verify-token', {
            headers: {
                'Authorization': `Bearer ${storedToken}`
            }
        }).then(response => {
            if (!response.ok) {
                throw new Error('Invalid token');
            }
            token = storedToken;
            document.getElementById('loginForm').classList.add('hidden');
            document.getElementById('mainApp').classList.remove('hidden');
            initializeWebSocket();
            loadTasks();
        }).catch(error => {
            // Token invalid - remove it and show login form
            localStorage.removeItem('token');
            token = null;
        });
    }
});

// Task Management
let tasks = [];

async function loadTasks() {
    try {
        const response = await fetch('/tasks', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        tasks = await response.json();
        renderTasks();
    } catch (error) {
        console.error('Failed to load tasks:', error);
    }
}

async function createTask() {
    const title = document.getElementById('taskTitle').value;
    const estimatedPomodoros = parseInt(document.getElementById('estimatedPomodoros').value);

    if (!title || !estimatedPomodoros) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('/tasks', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                estimated_pomodoros: estimatedPomodoros,
                description: ''
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create task');
        }

        const task = await response.json();
        tasks.push(task);
        renderTasks();
        
        document.getElementById('taskTitle').value = '';
        document.getElementById('estimatedPomodoros').value = '';
    } catch (error) {
        alert('Failed to create task: ' + error.message);
    }
}

async function deleteTask(taskId) {
    try {
        await fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        tasks = tasks.filter(t => t.id !== taskId);
        renderTasks();
    } catch (error) {
        alert('Failed to delete task');
    }
}

async function toggleTaskComplete(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    try {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...task,
                is_active: !task.is_active
            })
        });
        
        const updatedTask = await response.json();
        tasks = tasks.map(t => t.id === taskId ? updatedTask : t);
        renderTasks();
    } catch (error) {
        alert('Failed to update task');
    }
}

function moveTask(taskId, direction) {
    const index = tasks.findIndex(t => t.id === taskId);
    if (index === -1) return;
    
    if (direction === 'up' && index > 0) {
        [tasks[index], tasks[index - 1]] = [tasks[index - 1], tasks[index]];
    } else if (direction === 'down' && index < tasks.length - 1) {
        [tasks[index], tasks[index + 1]] = [tasks[index + 1], tasks[index]];
    }
    
    renderTasks();
}

function renderTasks() {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach((task, index) => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task-item p-4 bg-gray-50 rounded mb-2 ' + 
            (task.is_active ? '' : 'opacity-50');
        taskElement.innerHTML = `
            <div class="flex justify-between items-center">
                <div class="flex-1">
                    <h3 class="font-bold ${task.is_active ? '' : 'line-through'}">${task.title}</h3>
                    <p class="text-sm text-gray-600">
                        ${task.completed_pomodoros}/${task.estimated_pomodoros} Pomodoros
                    </p>
                    <div class="task-progress">
                        <div class="task-progress-bar" style="width: ${(task.completed_pomodoros / task.estimated_pomodoros) * 100}%"></div>
                    </div>
                </div>
                <div class="flex space-x-2">
                    ${index > 0 ? `
                        <button onclick="moveTask(${task.id}, 'up')" class="text-gray-600 hover:text-gray-800">↑</button>
                    ` : ''}
                    ${index < tasks.length - 1 ? `
                        <button onclick="moveTask(${task.id}, 'down')" class="text-gray-600 hover:text-gray-800">↓</button>
                    ` : ''}
                    <button onclick="toggleTaskComplete(${task.id})" class="text-blue-500 hover:text-blue-700">
                        ${task.is_active ? '✓' : '↺'}
                    </button>
                    <button onclick="deleteTask(${task.id})" class="text-red-500 hover:text-red-700">×</button>
                    <button onclick="selectTask(${task.id})" class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600">
                        Select
                    </button>
                </div>
            </div>
        `;
        taskList.appendChild(taskElement);
    });
}

function selectTask(taskId) {
    currentTask = tasks.find(t => t.id === taskId);
    document.getElementById('currentTaskName').textContent = currentTask ? currentTask.title : 'No task selected';
}

// Timer Functions
function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const display = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById('timer').textContent = display;
    
    // Update title for tab
    document.title = `${display} - Pomodoro`;
}

function startTimer() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').classList.add('hidden');
        document.getElementById('pauseBtn').classList.remove('hidden');

        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'start_session',
                data: {
                    task_id: currentTask?.id,
                    session_type: sessionType,
                    current_session_number: currentSessionNumber
                }
            }));
        }

        timerInterval = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateTimerDisplay();
                
                if (timeLeft <= 0) {
                    handleSessionComplete();
                }
            }
        }, 1000);
    }
}


// Timer Control Functions
function pauseTimer() {
    if (isRunning) {
        isRunning = false;
        clearInterval(timerInterval);
        document.getElementById('startBtn').classList.remove('hidden');
        document.getElementById('pauseBtn').classList.add('hidden');

        // Notify other devices about pause via WebSocket
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'pause_session'
            }));
        }
    }
}

function resetTimer() {
    // Reset timer to initial work session duration
    isRunning = false;
    clearInterval(timerInterval);
    sessionType = 'work';
    timeLeft = 25 * 60; // Default to 25 minutes
    updateTimerDisplay();
    updateSessionTypeDisplay();
    
    document.getElementById('startBtn').classList.remove('hidden');
    document.getElementById('pauseBtn').classList.add('hidden');
}

function handleSessionComplete() {
    // Stop the current timer
    clearInterval(timerInterval);
    isRunning = false;

    // Play notification sound and show browser notification
    playSound('break');
    sendNotification('Pomodoro Timer', 
        `${sessionType === 'work' ? 'Work session' : 'Break'} completed!`);

    // Notify server about session completion
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'end_session',
            data: { 
                session_id: currentSessionNumber,
                task_id: currentTask?.id
            }
        }));
    }

    // Update session type and timer duration
    if (sessionType === 'work') {
        // After work session, determine break type
        if (currentSessionNumber % 4 === 0) {
            sessionType = 'long_break';
            timeLeft = 15 * 60; // 15 minutes for long break
        } else {
            sessionType = 'short_break';
            timeLeft = 5 * 60; // 5 minutes for short break
        }
    } else {
        // After any break, start new work session
        sessionType = 'work';
        timeLeft = 25 * 60;
        if (sessionType === 'long_break') {
            currentSessionNumber = 1;
        } else {
            currentSessionNumber++;
        }

        // Update task progress if one is selected
        if (currentTask) {
            updateTaskProgress(currentTask.id);
        }
    }

    // Update displays
    updateTimerDisplay();
    updateSessionTypeDisplay();
    document.getElementById('startBtn').classList.remove('hidden');
    document.getElementById('pauseBtn').classList.add('hidden');
}

async function updateTaskProgress(taskId) {
    try {
        const task = tasks.find(t => t.id === taskId);
        if (!task) return;

        // Increment completed pomodoros
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...task,
                completed_pomodoros: task.completed_pomodoros + 1
            })
        });

        if (!response.ok) throw new Error('Failed to update task progress');

        // Update local task list and re-render
        const updatedTask = await response.json();
        tasks = tasks.map(t => t.id === taskId ? updatedTask : t);
        renderTasks();
    } catch (error) {
        console.error('Failed to update task progress:', error);
    }
}

function updateSessionTypeDisplay() {
    const sessionTypeElement = document.getElementById('sessionType');
    let displayText = '';
    let className = '';

    switch (sessionType) {
        case 'work':
            displayText = 'Work Session';
            className = 'work';
            break;
        case 'short_break':
            displayText = 'Short Break';
            className = 'break';
            break;
        case 'long_break':
            displayText = 'Long Break';
            className = 'long-break';
            break;
    }

    sessionTypeElement.textContent = displayText;
    sessionTypeElement.className = className;
}

// WebSocket Connection Management
function initializeWebSocket() {
    // Close existing connection if any
    if (ws) {
        ws.close();
    }

    // Create new WebSocket connection
    ws = new WebSocket(`ws://${window.location.host}/ws/${token}`);

    ws.onopen = () => {
        console.log('WebSocket connected');
        // Request current session state if any
        ws.send(JSON.stringify({ type: 'get_session_state' }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected. Attempting to reconnect...');
        // Attempt to reconnect after a delay
        setTimeout(initializeWebSocket, 3000);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'session_started':
            // Sync with remote timer state
            timeLeft = data.data.remaining_time;
            sessionType = data.data.session_type;
            currentSessionNumber = data.data.current_session;
            if (!isRunning) startTimer();
            break;

        case 'session_paused':
            if (isRunning) pauseTimer();
            break;

        case 'session_ended':
            handleSessionComplete();
            break;

        case 'session_state':
            // Update local state with server state
            if (data.data.active_session) {
                timeLeft = data.data.remaining_time;
                sessionType = data.data.session_type;
                currentSessionNumber = data.data.current_session;
                updateTimerDisplay();
                updateSessionTypeDisplay();
                if (data.data.is_running && !isRunning) {
                    startTimer();
                }
            }
            break;
    }
}