from datetime import datetime
import streamlit as st
from utils.state import add_activity_log
from utils.alerts import add_alert
from utils.contestants import get_active_contestants, get_contestant_by_name

def get_all_tasks():
    return st.session_state.get("tasks", [])

def get_task_by_id(tid):
    for t in get_all_tasks():
        if t["id"] == tid:
            return t
    return None

def create_task(name, description, assignee_type, assigned_to, reward, duration_min, deadline):
    """Create a new task in the command center."""
    if not name or not name.strip():
        return False, "Task name cannot be empty."
    if reward < 0:
        return False, "Reward points must be non-negative."
    if duration_min <= 0:
        return False, "Duration must be greater than 0 minutes."
        
    tasks = st.session_state.get("tasks", [])
    now_str = datetime.now().strftime("%I:%M %p")
    new_id = f"t-{len(tasks) + 1:02d}"
    
    new_task = {
        "id": new_id,
        "name": name.strip(),
        "description": description.strip() if description else "No description provided.",
        "assignee_type": assignee_type,
        "assigned_to": assigned_to,
        "points_reward": int(reward),
        "duration_min": int(duration_min),
        "deadline": deadline.strip() if deadline else "End of day",
        "status": "PENDING",
        "created_at": now_str,
        "completed_at": null if False else None
    }
    
    tasks.insert(0, new_task)
    add_activity_log(
        f"New Task created: '{name}' assigned to {assigned_to} (+{reward} pts).",
        log_type="TASK"
    )
    return True, f"Task '{name}' created successfully."

def start_task(task_id):
    """Mark a pending task as IN PROGRESS."""
    t = get_task_by_id(task_id)
    if not t:
        return False, "Task not found."
    if t["status"] == "COMPLETED":
        return False, "Completed task cannot be restarted."
    
    t["status"] = "IN PROGRESS"
    add_activity_log(f"Task '{t['name']}' started (IN PROGRESS).", log_type="TASK")
    return True, f"Task '{t['name']}' is now IN PROGRESS."

def complete_task(task_id):
    """
    Mark task complete and automatically award points to assigned contestant or team.
    RULE: Completed tasks cannot be completed twice.
    RULE: Evicted contestants cannot receive points.
    """
    t = get_task_by_id(task_id)
    if not t:
        return False, "Task not found."
    if t["status"] == "COMPLETED":
        return False, "Task is already completed."
    
    reward = t.get("points_reward", 0)
    assignee_type = t.get("assignee_type", "CONTESTANT")
    assigned_to = t.get("assigned_to", "")
    now_str = datetime.now().strftime("%I:%M %p")
    
    awarded_names = []
    
    if assignee_type == "CONTESTANT":
        target = get_contestant_by_name(assigned_to)
        if target and not target.get("evicted", False):
            target["points"] = target.get("points", 0) + reward
            target["tasks_completed"] = target.get("tasks_completed", 0) + 1
            awarded_names.append(f"{target['name']} (+{reward})")
    elif assignee_type == "TEAM":
        # Match team name (e.g. "Team Alpha" -> "Alpha", or exact match)
        target_team = assigned_to.replace("Team ", "").strip()
        active_members = [
            c for c in get_active_contestants()
            if c.get("team", "").lower() == target_team.lower()
        ]
        for m in active_members:
            m["points"] = m.get("points", 0) + reward
            m["tasks_completed"] = m.get("tasks_completed", 0) + 1
            awarded_names.append(f"{m['name']} (+{reward})")
            
    t["status"] = "COMPLETED"
    t["completed_at"] = now_str
    
    detail = f" Awarded points to: {', '.join(awarded_names)}" if awarded_names else " No active eligible contestants found."
    add_activity_log(
        f"Task '{t['name']}' marked COMPLETED.{detail}",
        log_type="TASK"
    )
    add_alert("INFO", "Task Completed", f"Task '{t['name']}' has been completed.{detail}", priority="MEDIUM", related_task=t['name'])
    return True, f"Task completed successfully!{detail}"

def delete_task(task_id):
    """Delete a task."""
    tasks = st.session_state.get("tasks", [])
    target = get_task_by_id(task_id)
    if not target:
        return False, "Task not found."
    
    st.session_state.tasks = [t for t in tasks if t["id"] != task_id]
    add_activity_log(f"Task '{target['name']}' was deleted.", log_type="TASK")
    return True, f"Task '{target['name']}' removed."
