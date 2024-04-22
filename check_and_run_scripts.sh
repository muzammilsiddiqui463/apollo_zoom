#!/bin/bash
# Function to check if a tmux session exists
check_tmux_session() {
    session_name=$1
    if tmux has-session -t "$session_name" 2>/dev/null; then
        return 0  # Session exists
    else
        return 1  # Session does not exist
    fi
}

# Function to check if a script is running
check_script_running() {
    script_name=$1
    if pgrep -f "python3 $script_name" >/dev/null; then
        return 0  # Script is running
    else
        return 1  # Script is not running
    fi
}

# Function to start a script in a tmux session
start_script() {
    session_name=$1
    script_name=$2
    tmux send-keys -t "$session_name" "/root/apollo_zoom/venv/bin/python3 $script_name" C-m
}

# Check if the tmux session exists
if check_tmux_session "apollo1"; then
    echo "Tmux session 'apollo1' exists"
else
    echo "Creating tmux session 'apollo1'"
    tmux new-session -d -s "apollo1"
fi

# Check and run script if session exists
if check_script_running "/root/apollo_zoom/apollo_boy1.py"; then
    echo "Apollo is already running"
else
    echo "Starting Apollo Script"
    start_script "apollo" "/root/apollo_zoom/apollo_boy1.py"
fi

# Check if the tmux session exists
if check_tmux_session "apollo2"; then
    echo "Tmux session 'apollo2' exists"
else
    echo "Creating tmux session 'apollo2'"
    tmux new-session -d -s "apollo2"
fi

# Check and run script if session exists
if check_script_running "/root/apollo_zoom/apollo_boy2.py"; then
    echo "Apollo is already running"
else
    echo "Starting Apollo Script"
    start_script "apollo" "/root/apollo_zoom/apollo_boy2.py"
fi

# Check if the tmux session exists
if check_tmux_session "apollo3"; then
    echo "Tmux session 'apollo3' exists"
else
    echo "Creating tmux session 'apollo3'"
    tmux new-session -d -s "apollo3"
fi

# Check and run script if session exists
if check_script_running "/root/apollo_zoom/apollo_boy3.py"; then
    echo "Apollo is already running"
else
    echo "Starting Apollo Script"
    start_script "apollo" "/root/apollo_zoom/apollo_boy3.py"
fi

# Check if the tmux session exists
if check_tmux_session "apollo_main"; then
    echo "Tmux session 'apollo_main' exists"
else
    echo "Creating tmux session 'apollo_main'"
    tmux new-session -d -s "apollo_main"
fi

# Check and run script if session exists
if check_script_running "/root/apollo_zoom/apollo_main_driver.py"; then
    echo "Apollo Main Driver is already running"
else
    echo "Starting Apollo Main Driver Script"
    start_script "apollo" "/root/apollo_zoom/apollo_main_driver.py"
fi
