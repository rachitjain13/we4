"""
BIG BOSS — HOUSE COMMAND CENTER
Strict Monochrome UI Components & Helpers
"""

import os
import streamlit as st
from utils.contestants import get_active_contestants, get_current_captain
from utils.alerts import get_unread_alerts_count

def apply_custom_styles():
    """Inject strict monochrome CSS styling."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def render_header():
    """
    Renders Executive Command Header.
    Left: BIG BOSS / HOUSE COMMAND CENTER
    Right: ● LIVE / CAPTAIN: ... / ACTIVE: ... / ALERTS: [...]
    Strictly monochrome with subtle white pulse.
    """
    captain = get_current_captain()
    cap_name = captain["name"].upper() if captain else "NONE ASSIGNED"
    active_count = len(get_active_contestants())
    unread_alerts = get_unread_alerts_count()

    header_html = f"""
    <div class="bb-header">
      <div class="bb-header-title-group">
        <h1>BIG BOSS</h1>
        <div class="bb-header-subtitle">HOUSE COMMAND CENTER</div>
      </div>
      <div class="bb-header-meta">
        <div class="bb-live-indicator">
          <span class="bb-pulse-dot"></span> LIVE
        </div>
        <div class="bb-meta-item">
          CAPTAIN: <strong>{cap_name}</strong>
        </div>
        <div class="bb-meta-item">
          ACTIVE: <strong>{active_count}</strong>
        </div>
        <div class="bb-meta-item">
          ALERTS: <strong>[{unread_alerts}]</strong>
        </div>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_toast():
    """Renders active monochrome toast notification if present."""
    toast_msg = st.session_state.get("active_toast")
    if toast_msg:
        toast_html = f"""
        <div class="bb-toast">
            <span>{toast_msg}</span>
        </div>
        """
        st.markdown(toast_html, unsafe_allow_html=True)
        # Clear after rendering so it displays for one run
        st.session_state.active_toast = None

def trigger_toast(message):
    """Sets a toast message for display."""
    st.session_state.active_toast = message

def render_announcement_banner():
    """Renders top announcement banner if an announcement is active."""
    current_ann = st.session_state.get("current_announcement")
    if current_ann and current_ann.get("active", True):
        priority = current_ann.get("priority", "Normal").upper()
        msg = current_ann.get("message", "")
        timestamp = current_ann.get("timestamp", "")

        col_banner, col_dismiss = st.columns([0.94, 0.06])
        with col_banner:
            banner_html = f"""
            <div class="bb-announcement-banner">
              <div>
                <div class="bb-announcement-tag">&bull; NEW BIG BOSS ANNOUNCEMENT [{priority}]</div>
                <div class="bb-announcement-msg">"{msg}"</div>
              </div>
              <div class="bb-announcement-time">{timestamp}</div>
            </div>
            """
            st.markdown(banner_html, unsafe_allow_html=True)
        with col_dismiss:
            if st.button("✕", key="dismiss_ann_btn", help="Dismiss Announcement"):
                st.session_state.current_announcement = None
                st.rerun()

def get_status_badge(status, is_captain=False, is_immune=False, is_nominated=False, evicted=False):
    """Generate HTML strict monochrome badge."""
    if evicted:
        return '<span class="badge-evicted">&#10005; EVICTED</span>'
    if is_captain:
        return '<span class="badge-captain">&#9819; CAPTAIN</span>'
    if is_immune:
        return '<span class="badge-immune">&#9673; IMMUNE</span>'
    if is_nominated:
        return '<span class="badge-nominated">&#9670; NOMINATED</span>'
    return '<span class="badge-active">&#9679; ACTIVE</span>'

def render_empty_state(title, description):
    """Render a clean empty state card in strict monochrome."""
    html = f"""
    <div class="bb-empty-state">
      <div class="bb-empty-title">{title}</div>
      <div class="bb-empty-desc">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
