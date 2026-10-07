"""
BIG BOSS — HOUSE COMMAND CENTER
Live Alert Messages & Notification Engine
"""

from datetime import datetime
import streamlit as st

def get_all_alerts():
    """Retrieve all alerts from session state."""
    return st.session_state.get("alerts", [])

def get_unread_alerts():
    """Retrieve only unread alerts."""
    return [a for a in get_all_alerts() if not a.get("read", False)]

def get_unread_alerts_count():
    """Count of unread actionable alerts."""
    return len(get_unread_alerts())

def add_alert(alert_type, title, message, priority="MEDIUM", related_contestant=None, related_task=None, related_question=None):
    """
    Generate an actionable system alert in real-time.
    Alert Types: INFO, WARNING, IMPORTANT, SUCCESS (all rendered in strict monochrome).
    Includes duplicate mitigation for identical recent alerts.
    """
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    # Duplicate check within the last 3 alerts
    recent_alerts = st.session_state.alerts[:3]
    for ra in recent_alerts:
        if ra.get("message") == message and ra.get("title") == title:
            return ra

    now_str = datetime.now().strftime("%I:%M %p")
    alert_id = f"alert_{len(st.session_state.alerts) + 1:03d}"

    new_alert = {
        "id": alert_id,
        "type": alert_type.upper(),  # INFO, WARNING, IMPORTANT, SUCCESS
        "title": title.strip(),
        "message": message.strip(),
        "timestamp": now_str,
        "priority": priority.upper(),  # LOW, MEDIUM, HIGH, CRITICAL
        "read": False,
        "related_contestant": related_contestant,
        "related_task": related_task,
        "related_question": related_question
    }

    # Newest alerts first
    st.session_state.alerts.insert(0, new_alert)
    if len(st.session_state.alerts) > 100:
        st.session_state.alerts = st.session_state.alerts[:100]

    return new_alert

def mark_alert_read(alert_id):
    """Mark a specific alert as read."""
    for a in get_all_alerts():
        if a["id"] == alert_id:
            a["read"] = True
            return True
    return False

def mark_all_alerts_read():
    """Mark all active alerts as read."""
    for a in get_all_alerts():
        a["read"] = True
    return True

def clear_old_alerts():
    """Clear alerts marked as read, preserving unread and historical activity logs."""
    if "alerts" in st.session_state:
        st.session_state.alerts = [a for a in st.session_state.alerts if not a.get("read", False)]
    return True
