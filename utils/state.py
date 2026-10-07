import json
import os
from datetime import datetime
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CONTESTANTS_FILE = os.path.join(DATA_DIR, "contestants.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

def load_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def init_session_state():
    """Initialize all session state variables if not already present."""
    if "initialized" not in st.session_state:
        # Load seed data
        st.session_state.contestants = load_json_file(CONTESTANTS_FILE)
        st.session_state.tasks = load_json_file(TASKS_FILE)
        
        # Initial announcements
        st.session_state.announcements = [
            {
                "id": "ann-01",
                "message": "All contestants must adhere to House Protocol. The Surveillance Grid is active.",
                "priority": "Important",
                "timestamp": "08:00 AM",
                "active": True
            }
        ]
        st.session_state.current_announcement = st.session_state.announcements[0]
        
        # Initial activity log
        st.session_state.activity_log = [
            {
                "time": "08:00 AM",
                "text": "BIG BOSS Command Center initialized. House systems operational.",
                "type": "SYSTEM"
            },
            {
                "time": "08:15 AM",
                "text": "Aarav completed 'Morning Fitness Endurance Drill' (+50 pts).",
                "type": "TASK"
            },
            {
                "time": "08:20 AM",
                "text": "Rahul confirmed as House Captain.",
                "type": "CAPTAINCY"
            },
            {
                "time": "08:30 AM",
                "text": "Aarav granted House Immunity.",
                "type": "IMMUNITY"
            }
        ]
        
        # Timer state
        st.session_state.timer_config_min = 20
        st.session_state.timer_config_sec = 0
        st.session_state.timer_remaining_sec = 1200 # 20 minutes default
        st.session_state.timer_running = False
        st.session_state.timer_last_tick = None
        st.session_state.timer_finished = False
        
        # Toast state
        st.session_state.active_toast = None
        
        # Confirmation states
        st.session_state.evict_confirm_id = None
        
        st.session_state.initialized = True

def add_activity_log(text, log_type="SYSTEM"):
    """Prepend a new event to the activity log."""
    now_str = datetime.now().strftime("%I:%M %p")
    entry = {
        "time": now_str,
        "text": text,
        "type": log_type
    }
    if "activity_log" in st.session_state:
        st.session_state.activity_log.insert(0, entry)
        if len(st.session_state.activity_log) > 100:
            st.session_state.activity_log = st.session_state.activity_log[:100]

def broadcast_announcement(message, priority="Normal"):
    """Broadcast an announcement across the system."""
    now_str = datetime.now().strftime("%I:%M %p")
    ann_id = f"ann-{len(st.session_state.announcements) + 1:02d}"
    ann = {
        "id": ann_id,
        "message": message,
        "priority": priority,
        "timestamp": now_str,
        "active": True
    }
    st.session_state.announcements.insert(0, ann)
    st.session_state.current_announcement = ann
    add_activity_log(f"BIG BOSS broadcasted [{priority.upper()}]: \"{message}\"", "ANNOUNCEMENT")
    return ann

def dismiss_current_announcement():
    st.session_state.current_announcement = None
