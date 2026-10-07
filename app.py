"""
BIG BOSS — HOUSE COMMAND CENTER
Complete Production-Grade Executive Operations Dashboard
STRICT BLACK & WHITE & NEUTRAL GRAY MONOCHROME SYSTEM
"""

import os
import time
from datetime import datetime
import pandas as pd
import streamlit as st

from utils.state import (
    init_session_state,
    add_activity_log,
    broadcast_announcement,
    dismiss_current_announcement,
)
from utils.contestants import (
    get_all_contestants,
    get_active_contestants,
    get_evicted_contestants,
    get_contestant_by_id,
    get_contestant_by_name,
    get_current_captain,
    set_captain,
    adjust_points,
    nominate_contestant,
    revoke_nomination,
    grant_immunity,
    remove_immunity,
    evict_contestant,
)
from utils.tasks import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    start_task,
    complete_task,
    delete_task,
)
from utils.questions import (
    get_all_questions,
    get_question_by_id,
    submit_answer,
    create_question,
    reset_question,
    delete_question,
    get_question_stats,
)
from utils.alerts import (
    get_all_alerts,
    get_unread_alerts,
    get_unread_alerts_count,
    add_alert,
    mark_alert_read,
    mark_all_alerts_read,
    clear_old_alerts,
)
from utils.analytics import (
    get_analytics_summary,
    get_contestant_performance_data,
    get_performance_spotlights,
    get_team_comparison_analytics,
)
from utils.ui import (
    apply_custom_styles,
    render_header,
    render_announcement_banner,
    render_toast,
    trigger_toast,
    get_status_badge,
    render_empty_state,
)

# Page configuration
st.set_page_config(
    page_title="BIG BOSS — HOUSE COMMAND CENTER",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize data and custom styles
init_session_state()
apply_custom_styles()

# Render persistent executive header and banners
render_header()
render_toast()
render_announcement_banner()

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #222222; margin-bottom: 1rem;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #666666; letter-spacing: 0.22em; text-transform: uppercase;">SURVEILLANCE UNIT</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff; letter-spacing: 0.06em;">BIG BOSS CENTRAL</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_options = [
        "▌ Overview",
        "▌ Contestants",
        "▌ Tasks",
        "▌ Leaderboard",
        "▌ Performance Analytics",
        "▌ Questions",
        "▌ Nominations",
        "▌ Danger Zone",
        "▌ Announcements",
        "▌ Alert Center",
        "▌ Control Room",
    ]

    selected_nav = st.radio(
        "NAVIGATION",
        nav_options,
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<div style='border-top: 1px solid #222222; margin: 1.25rem 0;'></div>", unsafe_allow_html=True)

    # Quick House Glance
    active_cnt = len(get_active_contestants())
    evicted_cnt = len(get_evicted_contestants())
    nom_cnt = len([c for c in get_active_contestants() if c.get("is_nominated", False)])
    unread_cnt = get_unread_alerts_count()
    captain = get_current_captain()

    st.markdown(
        f"""
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #777777; line-height: 1.9;">
            <div>&bull; ACTIVE: <strong style="color: #ffffff;">{active_cnt}</strong></div>
            <div>&bull; IN DANGER: <strong style="color: {'#ffffff' if nom_cnt > 0 else '#777777'}; font-weight: 800;">{nom_cnt}</strong></div>
            <div>&bull; ALERTS: <strong style="color: {'#ffffff' if unread_cnt > 0 else '#777777'}; font-weight: 800;">[{unread_cnt}]</strong></div>
            <div>&bull; EVICTED: <strong style="color: #aaaaaa;">{evicted_cnt}</strong></div>
            <div>&bull; CAPTAIN: <strong style="color: #ffffff;">{captain['name'].upper() if captain else 'NONE'}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='border-top: 1px solid #222222; margin: 1.25rem 0;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="padding: 0.5rem 0; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #555555; line-height: 1.6;">
            <div style="color: #ffffff; font-weight: 800; letter-spacing: 0.12em;">BIG BOSS CONTROL</div>
            <div style="color: #aaaaaa;">● SYSTEM ONLINE</div>
            <div>v2.5.0 &bull; MONOCHROME CORE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Wrapper for subtle 200ms page entrance animation
st.markdown("<div class='page-container'>", unsafe_allow_html=True)

# ==============================================================================
# VIEW 1: OVERVIEW DASHBOARD
# ==============================================================================
if "Overview" in selected_nav:
    st.markdown("### HOUSE STATUS OVERVIEW")

    active_contestants = get_active_contestants()
    evicted_contestants = get_evicted_contestants()
    all_tasks = get_all_tasks()
    completed_tasks = [t for t in all_tasks if t.get("status") == "COMPLETED"]
    nominees = [c for c in active_contestants if c.get("is_nominated", False)]
    immune_contestants = [c for c in active_contestants if c.get("is_immune", False)]
    captain = get_current_captain()

    # Calculate Highest Scorer
    if active_contestants:
        sorted_active = sorted(active_contestants, key=lambda x: x.get("points", 0), reverse=True)
        top_scorer = sorted_active[0]
        top_scorer_str = f"{top_scorer['name'].upper()} — {top_scorer['points']} PTS"
    else:
        top_scorer_str = "NONE"

    # KPI Metric Cards (Strict Monochrome)
    kpi_cols = st.columns(7)
    with kpi_cols[0]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Active Contestants</div>
              <div class="bb-kpi-val">{len(active_contestants)}</div>
              <div class="bb-kpi-sub">Total in House</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_cols[1]:
        cap_val = captain["name"].upper() if captain else "NONE"
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">House Captain</div>
              <div class="bb-kpi-val" style="font-size: 1.15rem;">{cap_val}</div>
              <div class="bb-kpi-sub">Executive Lead</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_cols[2]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Top Scorer</div>
              <div class="bb-kpi-val" style="font-size: 1.05rem;">{top_scorer_str}</div>
              <div class="bb-kpi-sub">Rank #01 Leader</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_cols[3]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Completed Tasks</div>
              <div class="bb-kpi-val">{len(completed_tasks)} / {len(all_tasks)}</div>
              <div class="bb-kpi-sub">Challenges Done</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_cols[4]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Nominees</div>
              <div class="bb-kpi-val">{len(nominees)}</div>
              <div class="bb-kpi-sub">In Danger Zone</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_cols[5]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Immune</div>
              <div class="bb-kpi-val">{len(immune_contestants)}</div>
              <div class="bb-kpi-sub">Shield Protected</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi_cols[6]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Evicted</div>
              <div class="bb-kpi-val">{len(evicted_contestants)}</div>
              <div class="bb-kpi-sub">Removed Housemates</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Danger Zone Notice if Nominees Exist (Strict Monochrome - NO RED)
    if nominees:
        nominee_names = ", ".join([c["name"].upper() for c in nominees])
        st.markdown(
            f"""
            <div style="background-color: #111111; border: 1px solid #ffffff; border-radius: 4px; padding: 0.85rem 1.15rem; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #ffffff;">
                    <strong>! CAUTION:</strong> {len(nominees)} CONTESTANT(S) CURRENTLY NOMINATED FOR EVICTION [{nominee_names}].
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #888888; text-transform: uppercase;">DANGER ZONE ACTIVE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Dual Column: Top Standings & Live Activity Feed
    col_left, col_right = st.columns([0.55, 0.45])

    with col_left:
        st.markdown("#### TOP HOUSEMATES STANDINGS")
        if active_contestants:
            sorted_active = sorted(active_contestants, key=lambda x: x.get("points", 0), reverse=True)
            for rank, c in enumerate(sorted_active[:6], start=1):
                badge_html = get_status_badge(
                    c.get("status"),
                    is_captain=c.get("is_captain", False),
                    is_immune=c.get("is_immune", False),
                    is_nominated=c.get("is_nominated", False),
                )
                rank_str = f"#{rank:02d}"
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; background-color: #181818; border: 1px solid #222222; border-radius: 4px; margin-bottom: 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 800; color: {'#ffffff' if rank == 1 else '#666666'}; min-width: 32px;">{rank_str}</span>
                            <div>
                                <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">{c['name'].upper()}</div>
                                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #666666;">TEAM {c['team'].upper()} &bull; {c.get('tasks_completed', 0)} TASKS COMPLETED</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.95rem; color: #ffffff;">{c['points']} PTS</span>
                            {badge_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            render_empty_state("NO ACTIVE CONTESTANTS", "All contestants have been evicted.")

    with col_right:
        st.markdown("#### LIVE ACTIVITY FEED")
        activities = st.session_state.get("activity_log", [])
        if activities:
            st.markdown('<div class="bb-card" style="padding: 0.5rem 0.75rem;">', unsafe_allow_html=True)
            for item in activities[:8]:
                st.markdown(
                    f"""
                    <div class="bb-feed-item">
                        <span class="bb-feed-time">{item['time']}</span>
                        <span class="bb-feed-type">{item['type']}</span>
                        <span class="bb-feed-text">{item['text']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            render_empty_state("NO LOGGED EVENTS", "No activity recorded yet.")


# ==============================================================================
# VIEW 2: CONTESTANT MANAGEMENT
# ==============================================================================
elif "Contestants" in selected_nav:
    st.markdown("### CONTESTANT ROSTER & MANAGEMENT")

    all_c = get_all_contestants()
    active_c = get_active_contestants()

    # Filter controls
    col_filter1, col_filter2 = st.columns([0.4, 0.6])
    with col_filter1:
        team_filter = st.selectbox("FILTER BY TEAM", ["ALL TEAMS", "ALPHA", "BETA"], key="c_team_filter")
    with col_filter2:
        status_filter = st.selectbox(
            "FILTER BY STATUS",
            ["ALL CONTESTANTS", "ACTIVE ONLY", "IMMUNE", "NOMINATED", "CAPTAIN", "EVICTED"],
            key="c_status_filter",
        )

    # Filtered list
    filtered = all_c
    if team_filter != "ALL TEAMS":
        filtered = [c for c in filtered if c.get("team", "").upper() == team_filter]
    if status_filter == "ACTIVE ONLY":
        filtered = [c for c in filtered if not c.get("evicted", False)]
    elif status_filter == "IMMUNE":
        filtered = [c for c in filtered if c.get("is_immune", False) and not c.get("evicted", False)]
    elif status_filter == "NOMINATED":
        filtered = [c for c in filtered if c.get("is_nominated", False) and not c.get("evicted", False)]
    elif status_filter == "CAPTAIN":
        filtered = [c for c in filtered if c.get("is_captain", False)]
    elif status_filter == "EVICTED":
        filtered = [c for c in filtered if c.get("evicted", False)]

    # Table Display
    c_records = []
    for c in filtered:
        status_label = "EVICTED" if c.get("evicted") else (
            "CAPTAIN" if c.get("is_captain") else (
                "IMMUNE" if c.get("is_immune") else (
                    "NOMINATED" if c.get("is_nominated") else "ACTIVE"
                )
            )
        )
        c_records.append({
            "ID": c["id"],
            "Name": c["name"].upper(),
            "Team": c["team"].upper(),
            "Points": c["points"],
            "Status": status_label,
            "Captain": "YES" if c.get("is_captain") else "NO",
            "Immune": "YES" if c.get("is_immune") else "NO",
            "Nominated": "YES" if c.get("is_nominated") else "NO",
            "Tasks Completed": c.get("tasks_completed", 0),
        })

    if c_records:
        df_c = pd.DataFrame(c_records)
        st.dataframe(
            df_c,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Points": st.column_config.NumberColumn(format="%d PTS"),
            },
        )
    else:
        render_empty_state("NO CONTESTANTS FOUND", "No contestants match the selected filter criteria.")

    st.markdown("<div style='border-top: 1px solid #222222; margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

    # OPERATIONAL MANAGEMENT DRAWER
    st.markdown("### MANAGE CONTESTANT ACTIONS")
    selectable_contestants = [c for c in all_c if not c.get("evicted", False)]

    if not selectable_contestants:
        st.warning("No active contestants available to manage.")
    else:
        contestant_names = [f"{c['name'].upper()} (ID: {c['id']} | TEAM {c['team'].upper()} | {c['points']} PTS)" for c in selectable_contestants]
        selected_idx = st.selectbox("SELECT CONTESTANT TO MANAGE", range(len(selectable_contestants)), format_func=lambda i: contestant_names[i])
        c_target = selectable_contestants[selected_idx]

        col_dossier, col_controls = st.columns([0.35, 0.65])

        with col_dossier:
            st.markdown(
                f"""
                <div class="bb-card">
                    <div class="bb-card-title">CONTESTANT PROFILE</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">{c_target['name'].upper()}</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #888888; margin-bottom: 0.75rem;">
                        ID: {c_target['id']} &bull; TEAM {c_target['team'].upper()}
                    </div>
                    <div style="margin-bottom: 0.6rem;">
                        {get_status_badge(c_target.get('status'), c_target.get('is_captain'), c_target.get('is_immune'), c_target.get('is_nominated'))}
                    </div>
                    <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; line-height: 1.8;">
                        <div>&bull; CURRENT POINTS: <strong style="color: #ffffff;">{c_target['points']} PTS</strong></div>
                        <div>&bull; HOUSE CAPTAIN: <strong style="color: #ffffff;">{'YES' if c_target.get('is_captain') else 'NO'}</strong></div>
                        <div>&bull; IMMUNITY: <strong style="color: #ffffff;">{'ACTIVE' if c_target.get('is_immune') else 'NONE'}</strong></div>
                        <div>&bull; NOMINATED: <strong style="color: #ffffff;">{'YES' if c_target.get('is_nominated') else 'NO'}</strong></div>
                        <div>&bull; TASKS COMPLETED: <strong style="color: #ffffff;">{c_target.get('tasks_completed', 0)}</strong></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_controls:
            manage_tabs = st.tabs(["1. Point Control", "2. Captaincy", "3. Immunity", "4. Nomination", "5. Eviction"])

            # Tab 1: Point Control
            with manage_tabs[0]:
                st.markdown("##### ADJUST POINTS")
                col_pt1, col_pt2 = st.columns([0.4, 0.6])
                with col_pt1:
                    point_amount = st.number_input("Points Delta", min_value=1, max_value=1000, value=50, step=10, key="m_pt_amt")
                with col_pt2:
                    point_reason = st.text_input("Reason / Justification", value="Challenge Victory", key="m_pt_reason")

                col_btn_add, col_btn_sub = st.columns(2)
                with col_btn_add:
                    if st.button(f"+ ADD {point_amount} POINTS", use_container_width=True, key="btn_add_pts"):
                        ok, msg = adjust_points(c_target["id"], point_amount, point_reason)
                        if ok:
                            trigger_toast(f"✓ +{point_amount} points added to {c_target['name']}")
                            st.rerun()
                        else:
                            st.error(msg)
                with col_btn_sub:
                    if st.button(f"− DEDUCT {point_amount} POINTS", use_container_width=True, key="btn_sub_pts"):
                        ok, msg = adjust_points(c_target["id"], -point_amount, point_reason)
                        if ok:
                            trigger_toast(f"✓ −{point_amount} points deducted from {c_target['name']}")
                            st.rerun()
                        else:
                            st.error(msg)

            # Tab 2: Captaincy
            with manage_tabs[1]:
                st.markdown("##### CAPTAINCY DELEGATION")
                if c_target.get("is_captain"):
                    st.info(f"{c_target['name'].upper()} is currently the House Captain.")
                else:
                    st.markdown(f"Appoint **{c_target['name'].upper()}** as the sole House Captain. Previous captain will immediately lose captaincy.")
                    if st.button(f"ASSIGN {c_target['name'].upper()} AS CAPTAIN", key="btn_assign_cap", use_container_width=True):
                        ok, msg = set_captain(c_target["id"])
                        if ok:
                            trigger_toast(f"✓ {c_target['name']} is now House Captain")
                            st.rerun()
                        else:
                            st.error(msg)

            # Tab 3: Immunity
            with manage_tabs[2]:
                st.markdown("##### IMMUNITY SHIELD")
                if c_target.get("is_immune"):
                    st.success(f"{c_target['name'].upper()} currently holds House Immunity.")
                    if st.button(f"REMOVE IMMUNITY FROM {c_target['name'].upper()}", key="btn_rem_imm", use_container_width=True):
                        ok, msg = remove_immunity(c_target["id"])
                        if ok:
                            trigger_toast(f"✓ Immunity removed from {c_target['name']}")
                            st.rerun()
                else:
                    st.markdown(f"Granting immunity to **{c_target['name'].upper()}** protects them from nominations. If currently nominated, they will be cleared from danger.")
                    imm_reason = st.text_input("Immunity Reason", value="Won immunity task", key="imm_reason_input")
                    if st.button(f"GRANT IMMUNITY TO {c_target['name'].upper()}", key="btn_grant_imm", use_container_width=True):
                        ok, msg = grant_immunity(c_target["id"], imm_reason)
                        if ok:
                            trigger_toast(f"✓ {c_target['name']} granted immunity")
                            st.rerun()

            # Tab 4: Nomination
            with manage_tabs[3]:
                st.markdown("##### NOMINATION FOR EVICTION")
                if c_target.get("is_immune"):
                    st.markdown(
                        f"""
                        <div style="background-color: #111111; border: 1px solid #444444; border-radius: 4px; padding: 0.85rem; margin-bottom: 0.75rem;">
                            <div style="font-weight: 800; color: #ffffff;">◉ IMMUNE — NOMINATION DISABLED</div>
                            <div style="font-size: 0.82rem; color: #888888; margin-top: 3px;">Cannot nominate {c_target['name'].upper()}: contestant holds House Immunity.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                elif c_target.get("is_nominated"):
                    st.warning(f"{c_target['name'].upper()} is already on the nomination block in Danger Zone.")
                    st.markdown(f"**Citation:** {c_target.get('nomination_reason', 'N/A')}")
                    if st.button(f"REVOKE NOMINATION FOR {c_target['name'].upper()}", key="btn_rev_nom", use_container_width=True):
                        ok, msg = revoke_nomination(c_target["id"], "Pardoned by Big Boss")
                        if ok:
                            trigger_toast(f"✓ Nomination revoked for {c_target['name']}")
                            st.rerun()
                else:
                    nom_reason = st.text_input("Citation / Reason", value="Breach of house protocol", key="c_nom_reason_val")
                    if st.button(f"NOMINATE {c_target['name'].upper()}", key="btn_nom_c", use_container_width=True):
                        ok, msg = nominate_contestant(c_target["id"], nom_reason)
                        if ok:
                            trigger_toast(f"✓ {c_target['name']} nominated")
                            st.rerun()
                        else:
                            st.error(msg)

            # Tab 5: Eviction
            with manage_tabs[4]:
                st.markdown("##### PERMANENT EVICTION")
                st.markdown(
                    f"""
                    <div style="background-color: #111111; border: 1px solid #444444; border-radius: 4px; padding: 0.85rem; margin-bottom: 0.75rem;">
                        <div style="font-weight: 800; color: #ffffff;">CONFIRMATION REQUIRED</div>
                        <div style="font-size: 0.82rem; color: #888888; margin-top: 4px; line-height: 1.5;">
                            Are you sure you want to evict <strong>{c_target['name'].upper()}</strong>?<br>
                            This will permanently remove the contestant from the active house, leaderboard, future tasks, and captaincy.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                ev_reason = st.text_input("Eviction Citation", value="Eliminated by public vote", key="tab_ev_reason")
                if st.button(f"CONFIRM EVICTION OF {c_target['name'].upper()}", key="tab_btn_evict", use_container_width=True):
                    ok, msg = evict_contestant(c_target["id"], ev_reason)
                    if ok:
                        trigger_toast(f"✓ {c_target['name']} evicted")
                        st.rerun()
                    else:
                        st.error(msg)


# ==============================================================================
# VIEW 3: TASK MANAGEMENT
# ==============================================================================
elif "Tasks" in selected_nav:
    st.markdown("### TASK & CHALLENGE MANAGEMENT")

    all_tasks = get_all_tasks()
    completed_t = [t for t in all_tasks if t.get("status") == "COMPLETED"]
    in_prog_t = [t for t in all_tasks if t.get("status") == "IN PROGRESS"]
    pending_t = [t for t in all_tasks if t.get("status") == "PENDING"]

    t_cols = st.columns(4)
    with t_cols[0]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Total Tasks</div>
              <div class="bb-kpi-val">{len(all_tasks)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t_cols[1]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Completed Tasks</div>
              <div class="bb-kpi-val">{len(completed_t)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t_cols[2]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">In Progress</div>
              <div class="bb-kpi-val">{len(in_prog_t)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t_cols[3]:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
              <div class="bb-kpi-label">Pending</div>
              <div class="bb-kpi-val">{len(pending_t)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # CREATE NEW TASK FORM
    with st.expander("＋ CREATE NEW CHALLENGE / TASK", expanded=False):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            t_name = st.text_input("Task Title", placeholder="e.g. Secret Room Ration Hunt")
            t_desc = st.text_area("Task Description", placeholder="Outline task instructions and criteria...")
            t_deadline = st.text_input("Deadline", value="Today 06:00 PM")

        with col_t2:
            t_assignee_type = st.radio("Assignee Target", ["TEAM", "CONTESTANT"], horizontal=True)
            if t_assignee_type == "TEAM":
                t_assigned_to = st.selectbox("Assign to Team", ["Team Alpha", "Team Beta"])
            else:
                active_names = [c["name"] for c in get_active_contestants()]
                t_assigned_to = st.selectbox("Assign to Contestant", active_names if active_names else ["None"])

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                t_reward = st.number_input("Reward Points", min_value=10, max_value=1000, value=100, step=10)
            with col_sub2:
                t_duration = st.number_input("Duration (Minutes)", min_value=5, max_value=300, value=30, step=5)

            if st.button("BROADCAST & CREATE TASK", use_container_width=True):
                ok, msg = create_task(
                    t_name,
                    t_desc,
                    t_assignee_type,
                    t_assigned_to,
                    t_reward,
                    t_duration,
                    t_deadline,
                )
                if ok:
                    trigger_toast(f"✓ Task '{t_name}' created")
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("#### ACTIVE HOUSE TASKS")

    if not all_tasks:
        render_empty_state("NO ACTIVE TASKS", "Create a task above to begin managing House activities.")
    else:
        for t in all_tasks:
            is_completed = t["status"] == "COMPLETED"
            card_border = "#ffffff" if is_completed else "#222222"

            col_card, col_action = st.columns([0.76, 0.24])
            with col_card:
                st.markdown(
                    f"""
                    <div style="background-color: #181818; border: 1px solid {card_border}; border-radius: 4px; padding: 1.15rem; margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                            <div>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #666666; text-transform: uppercase;">TASK #{t['id']} &bull; {t['assignee_type']}</span>
                                <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff;">{t['name']}</div>
                            </div>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; background-color: #111111; color: #ffffff; border: 1px solid {'#ffffff' if is_completed else '#444444'};">
                                {t['status']}
                            </span>
                        </div>
                        <div style="font-size: 0.86rem; color: #aaaaaa; margin-bottom: 0.75rem;">
                            {t['description']}
                        </div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #666666; display: flex; gap: 1.5rem; flex-wrap: wrap;">
                            <div>ASSIGNED: <strong style="color: #ffffff;">{t['assigned_to'].upper()}</strong></div>
                            <div>REWARD: <strong style="color: #ffffff;">+{t['points_reward']} PTS</strong></div>
                            <div>DURATION: <strong style="color: #ffffff;">{t['duration_min']} MIN</strong></div>
                            <div>DEADLINE: <strong style="color: #ffffff;">{t['deadline']}</strong></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_action:
                st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                if t["status"] == "PENDING":
                    if st.button("▶ START TASK", key=f"start_task_{t['id']}", use_container_width=True):
                        ok, msg = start_task(t["id"])
                        if ok:
                            trigger_toast(f"✓ Task '{t['name']}' started")
                            st.rerun()
                elif t["status"] == "IN PROGRESS":
                    if st.button("✔ MARK COMPLETE", key=f"complete_task_{t['id']}", use_container_width=True):
                        ok, msg = complete_task(t["id"])
                        if ok:
                            trigger_toast(f"✓ Task completed (+{t['points_reward']} pts awarded)")
                            st.rerun()

                if st.button("✕ DELETE", key=f"del_task_{t['id']}", use_container_width=True):
                    ok, msg = delete_task(t["id"])
                    if ok:
                        trigger_toast(f"✓ Task deleted")
                        st.rerun()


# ==============================================================================
# VIEW 4: LIVE LEADERBOARD
# ==============================================================================
elif "Leaderboard" in selected_nav:
    st.markdown("### LIVE HOUSE LEADERBOARD")
    st.markdown("Live ranking sorted strictly descending by total points. Evicted contestants are completely excluded.")

    active_contestants = get_active_contestants()
    if not active_contestants:
        render_empty_state("NO ACTIVE CONTESTANTS", "No active contestants remain on the leaderboard.")
    else:
        ranked_contestants = sorted(active_contestants, key=lambda x: x.get("points", 0), reverse=True)
        top_points = ranked_contestants[0]["points"] if ranked_contestants else 0

        # Team Standings
        alpha_pts = sum(c["points"] for c in active_contestants if c["team"].upper() == "ALPHA")
        beta_pts = sum(c["points"] for c in active_contestants if c["team"].upper() == "BETA")

        col_st1, col_st2 = st.columns(2)
        with col_st1:
            st.markdown(
                f"""
                <div class="bb-card" style="padding: 1rem 1.25rem;">
                    <div class="bb-kpi-label">TEAM ALPHA AGGREGATE</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono', monospace;">{alpha_pts} PTS</div>
                    <div class="bb-kpi-sub">{len([c for c in active_contestants if c['team'].upper() == 'ALPHA'])} ACTIVE MEMBERS</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_st2:
            st.markdown(
                f"""
                <div class="bb-card" style="padding: 1rem 1.25rem;">
                    <div class="bb-kpi-label">TEAM BETA AGGREGATE</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono', monospace;">{beta_pts} PTS</div>
                    <div class="bb-kpi-sub">{len([c for c in active_contestants if c['team'].upper() == 'BETA'])} ACTIVE MEMBERS</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        for rank, c in enumerate(ranked_contestants, start=1):
            is_top = rank == 1
            diff = top_points - c["points"]
            diff_str = "LEADER" if is_top else f"−{diff} PTS FROM #1"

            bg_color = "#1f1f1f" if is_top else "#181818"
            border_color = "#ffffff" if is_top else "#222222"

            badge_html = get_status_badge(
                c.get("status"),
                is_captain=c.get("is_captain", False),
                is_immune=c.get("is_immune", False),
                is_nominated=c.get("is_nominated", False),
            )

            st.markdown(
                f"""
                <div style="background-color: {bg_color}; border: 1px solid {border_color}; border-radius: 4px; padding: 1rem 1.5rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 1.5rem;">
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 900; color: {'#ffffff' if is_top else '#666666'}; min-width: 45px;">
                            #{rank:02d}
                        </div>
                        <div>
                            <div style="font-size: 1.05rem; font-weight: 800; color: #ffffff;">{c['name'].upper()}</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #666666;">
                                TEAM {c['team'].upper()} &bull; ID: {c['id']} &bull; {c.get('tasks_completed', 0)} TASKS COMPLETED
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 2rem;">
                        <div style="text-align: right;">
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 800; color: #ffffff;">
                                {c['points']} PTS
                            </div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #888888;">
                                {diff_str}
                            </div>
                        </div>
                        <div>
                            {badge_html}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================================
# VIEW: QUESTIONS / PUZZLE CHALLENGE
# ==============================================================================
elif "Questions" in selected_nav:
    st.markdown(
        """
        <div class="bb-question-banner">
            <div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #ffffff; letter-spacing: 0.04em;">&#127942; QUESTIONS</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #aaaaaa; margin-top: 3px;">
                    HOUSE CHALLENGE &bull; Solve the challenge questions to earn points.
                </div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #666666; text-transform: uppercase;">
                SURVEILLANCE CIPHER LAB
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    q_stats = get_question_stats()
    all_q = get_all_questions()

    # Progress KPI Row
    col_qp1, col_qp2, col_qp3 = st.columns(3)
    with col_qp1:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
                <div class="bb-kpi-label">Questions Progress</div>
                <div class="bb-kpi-val">{q_stats['solved']} / {q_stats['total']} SOLVED</div>
                <div class="bb-kpi-sub">Total challenges deciphered</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_qp2:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
                <div class="bb-kpi-label">Total Question Points</div>
                <div class="bb-kpi-val">{q_stats['points_awarded']:,} PTS</div>
                <div class="bb-kpi-sub">Points disbursed to solvers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_qp3:
        st.markdown(
            f"""
            <div class="bb-kpi-card">
                <div class="bb-kpi-label">Remaining Challenges</div>
                <div class="bb-kpi-val">{q_stats['remaining']}</div>
                <div class="bb-kpi-sub">Unsolved ciphers active</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # SOLVING CONTESTANT SELECTOR (Rule: Only active, non-evicted contestants)
    active_contestants = get_active_contestants()
    if not active_contestants:
        st.warning("No active contestants available to solve questions.")
        active_contestant = None
    else:
        col_c_sel, col_empty = st.columns([0.45, 0.55])
        with col_c_sel:
            c_options = [c["name"] for c in active_contestants]
            selected_solver_name = st.selectbox(
                "SOLVING CONTESTANT (Answers are scored for this housemate)",
                c_options,
                key="select_solving_contestant"
            )
            active_contestant = get_contestant_by_name(selected_solver_name)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # FILTERS & SEARCH ROW
    col_qsearch, col_qfilter, col_qtype = st.columns([0.45, 0.3, 0.25])
    with col_qsearch:
        search_query = st.text_input("Search questions...", placeholder="Filter by ID, content or type...", key="q_search_input")
    with col_qfilter:
        status_filter = st.selectbox("Status Filter", ["ALL", "UNSOLVED ONLY", "SOLVED ONLY"], key="q_status_filter")
    with col_qtype:
        type_filter = st.selectbox("Type Filter", ["ALL TYPES", "HEX", "ASCII", "SYMBOL", "TEXT", "IMAGE"], key="q_type_filter")

    # Filter questions list
    display_questions = all_q
    if search_query and search_query.strip():
        q_low = search_query.strip().lower()
        display_questions = [
            q for q in display_questions
            if q_low in q.get("title", "").lower() or q_low in q.get("content", "").lower() or q_low in q.get("type", "").lower() or (q.get("solved_by") and q_low in q.get("solved_by", "").lower())
        ]
    if status_filter == "UNSOLVED ONLY":
        display_questions = [q for q in display_questions if not q.get("solved", False)]
    elif status_filter == "SOLVED ONLY":
        display_questions = [q for q in display_questions if q.get("solved", False)]
    if type_filter != "ALL TYPES":
        display_questions = [q for q in display_questions if q.get("type", "").lower() == type_filter.lower()]

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # QUESTION CARDS
    if not display_questions:
        render_empty_state("NO QUESTIONS FOUND", "No questions match your current search and filter settings.")
    else:
        for q in display_questions:
            is_solved = q.get("solved", False)
            card_class = "bb-question-card solved" if is_solved else "bb-question-card"

            st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
            
            # Top row of Question card
            col_qhead, col_qmeta = st.columns([0.7, 0.3])
            with col_qhead:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: baseline; gap: 0.75rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 900; color: #ffffff;">{q.get('title', 'Q')}</span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 3px; background-color: #111111; border: 1px solid #333333; color: #aaaaaa; text-transform: uppercase;">
                            {q.get('type', 'TEXT').upper()}
                        </span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #666666;">
                            {q.get('hint', '')}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_qmeta:
                st.markdown(
                    f"""
                    <div class="bb-reward-meta">
                        <div class="bb-reward-pts">+{q.get('points', 500)} ANSWER</div>
                        <div class="bb-reward-sub">UP TO {q.get('max_points', 1000)} BUILD</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Content area
            if q.get("type") in ["hex", "ascii", "symbol"]:
                st.markdown(f"<div class='bb-puzzle-code'>{q.get('content')}</div>", unsafe_allow_html=True)
            elif q.get("type") == "image":
                st.markdown(f"<div style='font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 0.75rem 0;'>{q.get('content')}</div>", unsafe_allow_html=True)
                img_path = q.get("image_path")
                if img_path and os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
            else:
                st.markdown(f"<div style='font-size: 1.05rem; font-weight: 600; color: #ffffff; margin: 0.85rem 0;'>{q.get('content')}</div>", unsafe_allow_html=True)

            # Feedback & Submission area
            if is_solved:
                st.markdown(
                    f"""
                    <div style="background-color: #111111; border: 1px solid #333333; border-radius: 4px; padding: 0.85rem 1rem; margin-top: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 800; color: #ffffff; font-size: 0.95rem;">&#10003; SOLVED</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #888888; margin-top: 2px;">
                                SOLVED BY: <strong style="color: #ffffff;">{q.get('solved_by', 'CONTESTANT')}</strong> &bull; {q.get('solved_at', 'Completed')}
                            </div>
                        </div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 800; color: #ffffff;">
                            REWARD: +{q.get('points', 500)} POINTS
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                # Question feedback alert
                fb = st.session_state.question_feedback.get(q["id"])
                if fb:
                    if fb.get("correct"):
                        st.markdown(
                            f"""
                            <div style="background-color: #181818; border: 1px solid #ffffff; border-radius: 4px; padding: 0.65rem 0.85rem; font-size: 0.85rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;">
                                {fb.get('msg')}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="bb-shake" style="background-color: #111111; border: 1px solid #444444; border-radius: 4px; padding: 0.65rem 0.85rem; font-size: 0.85rem; font-weight: 700; color: #cccccc; margin-bottom: 0.5rem;">
                                {fb.get('msg')}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                col_inp, col_sub = st.columns([0.78, 0.22])
                with col_inp:
                    ans_input = st.text_input(
                        "Your answer",
                        placeholder="Type answer here...",
                        key=f"input_{q['id']}",
                        label_visibility="collapsed"
                    )
                with col_sub:
                    if st.button("SUBMIT", key=f"btn_sub_{q['id']}", use_container_width=True):
                        if not active_contestant:
                            st.error("No active contestant selected.")
                        else:
                            ok, msg, pts = submit_answer(q["id"], active_contestant["id"], ans_input)
                            if ok:
                                st.session_state.question_feedback[q["id"]] = {"correct": True, "msg": msg}
                                trigger_toast(f"✓ {active_contestant['name']} solved {q.get('title', q['id'])} (+{pts} pts)")
                                st.rerun()
                            else:
                                st.session_state.question_feedback[q["id"]] = {"correct": False, "msg": msg}
                                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='border-top: 1px solid #222222; margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

    # QUESTION MANAGEMENT — BIG BOSS
    with st.expander("＋ QUESTION CONTROL — CREATE & MANAGE CHALLENGES", expanded=False):
        st.markdown("##### CREATE NEW CHALLENGE QUESTION")
        col_cq1, col_cq2 = st.columns(2)
        with col_cq1:
            cq_title = st.text_input("Question Identifier", value=f"Q{len(all_q)+1}", key="cq_title")
            cq_type = st.selectbox("Question Type", ["Hexadecimal", "ASCII / Number Sequence", "Morse / Symbol", "Text", "Image"], key="cq_type")
            cq_content = st.text_area("Question Content / Code / Clue", placeholder="Enter the cipher text, sequence, or riddle...", key="cq_content")
            cq_hint = st.text_input("Hint / Category Note", placeholder="Brief context clue...", key="cq_hint")

        with col_cq2:
            cq_answer = st.text_input("Expected Correct Answer", placeholder="Exact answer string...", key="cq_answer")
            col_pts1, col_pts2 = st.columns(2)
            with col_pts1:
                cq_points = st.number_input("Base Points", min_value=50, max_value=2000, value=500, step=50, key="cq_points")
            with col_pts2:
                cq_max_pts = st.number_input("Maximum Points", min_value=50, max_value=5000, value=1000, step=50, key="cq_max_pts")
            cq_case_sens = st.checkbox("Case Sensitive Answer", value=False, key="cq_case_sens")
            cq_img = st.text_input("Image Asset Path (optional)", placeholder="e.g. assets/blueprint.svg", key="cq_img")

            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("CREATE QUESTION", use_container_width=True, key="btn_create_q"):
                type_map = {
                    "Hexadecimal": "hex",
                    "ASCII / Number Sequence": "ascii",
                    "Morse / Symbol": "symbol",
                    "Text": "text",
                    "Image": "image"
                }
                ok, msg = create_question(
                    title=cq_title,
                    qtype=type_map.get(cq_type, "text"),
                    content=cq_content,
                    answer=cq_answer,
                    points=cq_points,
                    max_points=cq_max_pts,
                    hint=cq_hint,
                    case_sensitive=cq_case_sens,
                    image_path=cq_img if cq_img else None
                )
                if ok:
                    trigger_toast(f"✓ {cq_title} created successfully")
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("<div style='border-top: 1px solid #222222; margin: 1rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("##### MANAGE EXISTING QUESTIONS")
        if not all_q:
            st.info("No questions to manage.")
        else:
            q_manage_options = [f"{q.get('title', q['id'])} ({q.get('type', 'text').upper()} | {q.get('points')} pts | {'SOLVED by ' + str(q.get('solved_by')) if q.get('solved') else 'UNSOLVED'})" for q in all_q]
            selected_mq_idx = st.selectbox("Select Question to Manage", range(len(all_q)), format_func=lambda i: q_manage_options[i], key="sel_mq")
            target_mq = all_q[selected_mq_idx]

            col_btn_reset, col_btn_del = st.columns(2)
            with col_btn_reset:
                if st.button(f"RESET {target_mq.get('title', target_mq['id'])} TO UNSOLVED", key="btn_reset_mq", use_container_width=True):
                    ok, msg = reset_question(target_mq["id"])
                    if ok:
                        trigger_toast(f"✓ {target_mq.get('title', target_mq['id'])} reset to unsolved")
                        st.rerun()
            with col_btn_del:
                if st.button(f"DELETE {target_mq.get('title', target_mq['id'])}", key="btn_del_mq", use_container_width=True):
                    ok, msg = delete_question(target_mq["id"])
                    if ok:
                        trigger_toast(f"✓ {target_mq.get('title', target_mq['id'])} deleted")
                        st.rerun()


# ==============================================================================
# VIEW 5: NOMINATIONS
# ==============================================================================
elif "Nominations" in selected_nav:
    st.markdown("### NOMINATION CONTROL ROOM")
    st.markdown("Direct nomination desk. **Rule: Immune contestants CANNOT be nominated under any circumstances.**")

    active_contestants = get_active_contestants()
    immune_contestants = [c for c in active_contestants if c.get("is_immune", False)]
    nominees = [c for c in active_contestants if c.get("is_nominated", False)]

    col_nom_form, col_imm_list = st.columns([0.6, 0.4])

    with col_nom_form:
        st.markdown("#### NOMINATE CONTESTANT")
        if not active_contestants:
            st.warning("No active contestants available.")
        else:
            c_options = [c["name"] for c in active_contestants]
            selected_name = st.selectbox("Select Contestant to Nominate", c_options, key="nom_page_select")
            target = get_contestant_by_name(selected_name)

            if target:
                if target.get("is_immune", False):
                    st.markdown(
                        f"""
                        <div style="background-color: #111111; border: 1px solid #444444; border-radius: 4px; padding: 1rem; margin-bottom: 1rem;">
                            <div style="font-weight: 800; color: #ffffff;">◉ IMMUNE — NOMINATION DISABLED</div>
                            <div style="font-size: 0.84rem; color: #aaaaaa; margin-top: 4px;">
                                {target['name'].upper()} holds House Immunity. Big Boss rules forbid nominating an immune contestant.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                elif target.get("is_nominated", False):
                    st.markdown(
                        f"""
                        <div style="background-color: #111111; border: 1px solid #444444; border-radius: 4px; padding: 1rem; margin-bottom: 1rem;">
                            <div style="font-weight: 800; color: #ffffff;">ALREADY IN DANGER ZONE</div>
                            <div style="font-size: 0.84rem; color: #aaaaaa; margin-top: 4px;">
                                {target['name'].upper()} is already on the eviction block. Duplicate nominations are prevented.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    nom_reason = st.text_input("Formal Nomination Citation", value="Rule infraction / poor task effort", key="nom_pg_reason")
                    if st.button(f"NOMINATE {target['name'].upper()} FOR EVICTION", key="btn_do_nom_pg", use_container_width=True):
                        ok, msg = nominate_contestant(target["id"], nom_reason)
                        if ok:
                            trigger_toast(f"✓ {target['name']} nominated")
                            st.rerun()
                        else:
                            st.error(msg)

    with col_imm_list:
        st.markdown("#### IMMUNITY SHIELD REGISTRY")
        if immune_contestants:
            for imm in immune_contestants:
                st.markdown(
                    f"""
                    <div style="background-color: #181818; border: 1px solid #333333; border-radius: 4px; padding: 0.85rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 800; color: #ffffff;">{imm['name'].upper()}</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #777777;">TEAM {imm['team'].upper()} &bull; {imm['points']} PTS</div>
                        </div>
                        <span class="badge-immune">&#9673; IMMUNE</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            render_empty_state("NO IMMUNE CONTESTANTS", "No contestants currently possess immunity.")

    st.markdown("<div style='border-top: 1px solid #222222; margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("#### CURRENT NOMINEES LIST")

    if nominees:
        for nom in nominees:
            col_nc, col_na = st.columns([0.75, 0.25])
            with col_nc:
                st.markdown(
                    f"""
                    <div class="bb-danger-card">
                        <div class="bb-danger-header">
                            <div>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #888888;">NOMINATED CANDIDATE</span>
                                <div class="bb-danger-name">{nom['name'].upper()}</div>
                            </div>
                            <span class="bb-danger-badge">&#9670; NOMINATED</span>
                        </div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #aaaaaa; margin-top: 0.5rem; line-height: 1.6;">
                            <div>CITATION: <strong style="color: #ffffff;">{nom.get('nomination_reason', 'Disciplinary action')}</strong></div>
                            <div>NOMINATED AT: <strong>{nom.get('nomination_time', 'Today')}</strong></div>
                            <div>POINTS AT RISK: <strong>{nom['points']} PTS</strong> &bull; TEAM {nom['team'].upper()}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_na:
                st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
                if st.button("PARDON / REVOKE", key=f"rev_pg_{nom['id']}", use_container_width=True):
                    ok, msg = revoke_nomination(nom["id"], "Big Boss granted pardon.")
                    if ok:
                        trigger_toast(f"✓ Nomination revoked for {nom['name']}")
                        st.rerun()
                if st.button("GRANT IMMUNITY", key=f"grant_imm_pg_{nom['id']}", use_container_width=True):
                    ok, msg = grant_immunity(nom["id"], "Big Boss immunity grant")
                    if ok:
                        trigger_toast(f"✓ Immunity granted to {nom['name']}")
                        st.rerun()
    else:
        render_empty_state("NO NOMINEES", "No contestants are currently in the Danger Zone.")


# ==============================================================================
# VIEW 6: DANGER ZONE
# ==============================================================================
elif "Danger Zone" in selected_nav:
    st.markdown("### ! DANGER ZONE — CURRENT NOMINEES")
    st.markdown("Eviction containment block. Contestants listed here are at immediate risk of elimination.")

    active_contestants = get_active_contestants()
    nominees = [c for c in active_contestants if c.get("is_nominated", False)]

    if not nominees:
        render_empty_state(
            "NO CONTESTANTS CURRENTLY IN DANGER",
            "The eviction block is clear. All Housemates are currently safe from elimination."
        )
    else:
        st.markdown(
            f"""
            <div class="bb-danger-container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 800; color: #ffffff;">
                        ! ATTENTION: {len(nominees)} HOUSEMATE(S) MARKED FOR EVICTION
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #888888;">
                        SURVEILLANCE LEVEL 5 &bull; MONOCHROME CONTAINMENT
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        for nom in nominees:
            col_card, col_actions = st.columns([0.72, 0.28])
            with col_card:
                st.markdown(
                    f"""
                    <div class="bb-danger-card">
                        <div class="bb-danger-header">
                            <div>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #888888; text-transform: uppercase;">TEAM {nom['team'].upper()} &bull; ID: {nom['id']}</span>
                                <div class="bb-danger-name">{nom['name'].upper()}</div>
                            </div>
                            <span class="bb-danger-badge">&#9670; NOMINATED</span>
                        </div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #aaaaaa; margin-top: 0.6rem; line-height: 1.7;">
                            <div>&bull; CITATION: <strong style="color: #ffffff;">{nom.get('nomination_reason', 'Disciplinary citation')}</strong></div>
                            <div>&bull; TIME OF CITATION: <strong>{nom.get('nomination_time', 'Today')}</strong></div>
                            <div>&bull; TOTAL POINTS AT RISK: <strong style="color: #ffffff;">{nom['points']} PTS</strong></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_actions:
                st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
                if st.button("PARDON / REVOKE NOMINATION", key=f"dz_pardon_{nom['id']}", use_container_width=True):
                    ok, msg = revoke_nomination(nom["id"], "Pardoned by Big Boss")
                    if ok:
                        trigger_toast(f"✓ Nomination revoked for {nom['name']}")
                        st.rerun()

                if st.button("CONFIRM EVICTION", key=f"dz_evict_{nom['id']}", use_container_width=True):
                    ok, msg = evict_contestant(nom["id"], f"Evicted from Danger Zone. Citation: {nom.get('nomination_reason')}")
                    if ok:
                        trigger_toast(f"✓ {nom['name']} evicted")
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 7: ANNOUNCEMENTS
# ==============================================================================
elif "Announcements" in selected_nav:
    st.markdown("### BIG BOSS BROADCAST & ANNOUNCEMENT CENTER")
    st.markdown("Broadcast official directives across the House. Broadcasts appear in persistent executive banners.")

    col_form, col_status = st.columns([0.65, 0.35])

    with col_form:
        st.markdown("#### NEW DIRECTIVE")
        ann_text = st.text_area(
            "Announcement Content",
            placeholder="Type your official directive here (e.g. 'All contestants must assemble in the living room immediately.')...",
            height=110,
        )

        col_prio, col_send = st.columns([0.5, 0.5])
        with col_prio:
            ann_prio = st.selectbox("Priority Level", ["Normal", "Important", "Critical"])
        with col_send:
            st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
            if st.button("BROADCAST ANNOUNCEMENT", use_container_width=True):
                if not ann_text or not ann_text.strip():
                    st.error("Announcement content cannot be empty.")
                else:
                    broadcast_announcement(ann_text.strip(), ann_prio)
                    trigger_toast("✓ Announcement broadcasted across House feeds")
                    st.rerun()

    with col_status:
        st.markdown("#### CURRENT ACTIVE BANNER")
        curr = st.session_state.get("current_announcement")
        if curr and curr.get("active", True):
            st.markdown(
                f"""
                <div class="bb-card">
                    <div class="bb-announcement-tag">&bull; ACTIVE &bull; [{curr['priority'].upper()}]</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 0.5rem 0;">"{curr['message']}"</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #666666;">{curr['timestamp']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("DISMISS ACTIVE BROADCAST", use_container_width=True):
                dismiss_current_announcement()
                st.rerun()
        else:
            render_empty_state("NO ACTIVE BROADCAST", "No announcement is currently pinned to the banner.")

    st.markdown("<div style='border-top: 1px solid #222222; margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("#### ANNOUNCEMENT HISTORY (NEWEST FIRST)")

    history = st.session_state.get("announcements", [])
    if history:
        for item in history:
            st.markdown(
                f"""
                <div style="background-color: #181818; border: 1px solid #222222; border-radius: 4px; padding: 0.95rem 1.15rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #aaaaaa; font-weight: 700; text-transform: uppercase;">
                            [{item['priority'].upper()}] &bull; DIRECTIVE #{item['id']}
                        </div>
                        <div style="font-size: 0.92rem; font-weight: 600; color: #ffffff; margin-top: 3px;">
                            "{item['message']}"
                        </div>
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #666666; text-align: right; min-width: 90px;">
                        {item['timestamp']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        render_empty_state("NO ANNOUNCEMENTS", "Big Boss has not broadcast anything yet.")


# ==============================================================================
# VIEW 8: CONTROL ROOM (TIMER, STATISTICS, EVICTION, ACTIVITY LEDGER)
# ==============================================================================
elif "Control Room" in selected_nav:
    st.markdown("### BIG BOSS MASTER CONTROL ROOM")
    st.markdown("Master control interface: Task Countdown Timer, Comprehensive House Analytics, Eviction Registry, and Global Activity Ledger.")

    tab_timer, tab_stats, tab_evict, tab_log = st.tabs([
        "1. Task Timer",
        "2. House Statistics",
        "3. Eviction Registry",
        "4. Full Activity Ledger",
    ])

    # --------------------------------------------------------------------------
    # TAB 1: TASK COUNTDOWN TIMER
    # --------------------------------------------------------------------------
    with tab_timer:
        st.markdown("#### LIVE TASK COUNTDOWN TIMER")
        st.markdown("Streamlit native non-blocking timer fragment. Ticks live every second.")

        @st.fragment(run_every="1s" if st.session_state.get("timer_running", False) else None)
        def render_timer_fragment():
            if st.session_state.get("timer_running", False):
                now = time.time()
                last = st.session_state.get("timer_last_tick", now)
                elapsed = int(now - last)
                if elapsed >= 1:
                    st.session_state.timer_remaining_sec = max(0, st.session_state.timer_remaining_sec - elapsed)
                    st.session_state.timer_last_tick = now

                # Timer expiration trigger
                if st.session_state.timer_remaining_sec <= 0:
                    st.session_state.timer_running = False
                    st.session_state.timer_finished = True
                    broadcast_announcement("TIME'S UP. THE TASK HAS ENDED.", "Critical")
                    add_activity_log("TASK TIMER EXPIRED: 'Time's Up' broadcasted.", "TASK")

            rem = st.session_state.get("timer_remaining_sec", 1200)
            mins = rem // 60
            secs = rem % 60
            digits_str = f"{mins:02d}:{secs:02d}"

            status_label = (
                "TIME'S UP — TASK CONCLUDED"
                if st.session_state.get("timer_finished", False) and rem == 0
                else ("RUNNING" if st.session_state.get("timer_running", False) else "STOPPED / READY")
            )

            st.markdown(
                f"""
                <div class="bb-timer-screen">
                    <div class="bb-timer-digits">{digits_str}</div>
                    <div class="bb-timer-label" style="font-weight: 800; color: #ffffff;">
                        ● {status_label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        render_timer_fragment()

        col_ctl1, col_ctl2, col_ctl3 = st.columns(3)
        with col_ctl1:
            if not st.session_state.get("timer_running", False):
                if st.button("▶ START COUNTDOWN", use_container_width=True, key="timer_start_btn"):
                    if st.session_state.get("timer_remaining_sec", 0) <= 0:
                        tot = st.session_state.timer_config_min * 60 + st.session_state.timer_config_sec
                        st.session_state.timer_remaining_sec = tot
                    st.session_state.timer_running = True
                    st.session_state.timer_last_tick = time.time()
                    st.session_state.timer_finished = False
                    add_activity_log("Task Countdown started.", "TASK")
                    st.rerun()
            else:
                if st.button("⏸ PAUSE COUNTDOWN", use_container_width=True, key="timer_pause_btn"):
                    st.session_state.timer_running = False
                    add_activity_log("Task Countdown paused.", "TASK")
                    st.rerun()

        with col_ctl2:
            if st.button("⏹ RESET TIMER", use_container_width=True, key="timer_reset_btn"):
                st.session_state.timer_running = False
                tot = st.session_state.timer_config_min * 60 + st.session_state.timer_config_sec
                st.session_state.timer_remaining_sec = tot
                st.session_state.timer_finished = False
                add_activity_log("Task Countdown reset.", "TASK")
                st.rerun()

        with col_ctl3:
            if st.button("TRIGGER TIME'S UP NOW", use_container_width=True, key="timer_force_zero"):
                st.session_state.timer_remaining_sec = 0
                st.session_state.timer_running = False
                st.session_state.timer_finished = True
                broadcast_announcement("TIME'S UP. THE TASK HAS ENDED.", "Critical")
                add_activity_log("Big Boss manually triggered TIME'S UP.", "TASK")
                st.rerun()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        with st.expander("CONFIGURE TIMER DURATION", expanded=False):
            col_m, col_s = st.columns(2)
            with col_m:
                cfg_min = st.number_input("Minutes", min_value=0, max_value=120, value=st.session_state.timer_config_min)
            with col_s:
                cfg_sec = st.number_input("Seconds", min_value=0, max_value=59, value=st.session_state.timer_config_sec)

            if st.button("APPLY TIMER DURATION", key="apply_timer_cfg"):
                st.session_state.timer_config_min = int(cfg_min)
                st.session_state.timer_config_sec = int(cfg_sec)
                st.session_state.timer_remaining_sec = int(cfg_min * 60 + cfg_sec)
                st.session_state.timer_running = False
                st.session_state.timer_finished = False
                trigger_toast(f"✓ Timer duration set to {cfg_min:02d}:{cfg_sec:02d}")
                st.rerun()

    # --------------------------------------------------------------------------
    # TAB 2: HOUSE STATISTICS & ANALYTICS
    # --------------------------------------------------------------------------
    with tab_stats:
        st.markdown("#### COMPREHENSIVE HOUSE ANALYTICS")

        all_contestants = get_all_contestants()
        active_contestants = get_active_contestants()
        evicted_contestants = get_evicted_contestants()
        all_tasks = get_all_tasks()
        completed_tasks = [t for t in all_tasks if t.get("status") == "COMPLETED"]
        pending_tasks = [t for t in all_tasks if t.get("status") == "PENDING"]
        nominees = [c for c in active_contestants if c.get("is_nominated", False)]
        immune_c = [c for c in active_contestants if c.get("is_immune", False)]
        captain = get_current_captain()

        if active_contestants:
            sorted_by_pts = sorted(active_contestants, key=lambda x: x.get("points", 0), reverse=True)
            highest_scorer = f"{sorted_by_pts[0]['name'].upper()} ({sorted_by_pts[0]['points']} PTS)"
            lowest_scorer = f"{sorted_by_pts[-1]['name'].upper()} ({sorted_by_pts[-1]['points']} PTS)"
            avg_pts = round(sum(c["points"] for c in active_contestants) / len(active_contestants), 1)
            total_points = sum(c["points"] for c in active_contestants)
        else:
            highest_scorer = "NONE"
            lowest_scorer = "NONE"
            avg_pts = 0
            total_points = 0

        # 12 Mandatory Analytics KPIs
        stat_cols1 = st.columns(4)
        with stat_cols1[0]:
            st.metric("HIGHEST SCORER", highest_scorer)
        with stat_cols1[1]:
            st.metric("LOWEST SCORER", lowest_scorer)
        with stat_cols1[2]:
            st.metric("AVERAGE HOUSE POINTS", f"{avg_pts} PTS")
        with stat_cols1[3]:
            st.metric("TOTAL POINTS AWARDED", f"{total_points:,} PTS")

        stat_cols2 = st.columns(4)
        with stat_cols2[0]:
            st.metric("ACTIVE CONTESTANTS", len(active_contestants))
        with stat_cols2[1]:
            st.metric("EVICTED CONTESTANTS", len(evicted_contestants))
        with stat_cols2[2]:
            st.metric("CURRENT CAPTAIN", captain["name"].upper() if captain else "NONE")
        with stat_cols2[3]:
            st.metric("IMMUNE CONTESTANTS", len(immune_c))

        stat_cols3 = st.columns(4)
        with stat_cols3[0]:
            st.metric("TOTAL TASKS", len(all_tasks))
        with stat_cols3[1]:
            st.metric("COMPLETED TASKS", len(completed_tasks))
        with stat_cols3[2]:
            st.metric("PENDING TASKS", len(pending_tasks))
        with stat_cols3[3]:
            st.metric("NOMINEES IN DANGER", len(nominees))

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### QUESTIONS & CHALLENGE ANALYTICS")
        q_stats = get_question_stats()
        stat_cols4 = st.columns(4)
        with stat_cols4[0]:
            st.metric("QUESTIONS SOLVED", f"{q_stats['solved']} / {q_stats['total']}")
        with stat_cols4[1]:
            st.metric("QUESTIONS REMAINING", q_stats["remaining"])
        with stat_cols4[2]:
            st.metric("QUESTION POINTS AWARDED", f"{q_stats['points_awarded']:,} PTS")
        with stat_cols4[3]:
            st.metric("TOP QUESTION SOLVER", q_stats["top_solver"])

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### POINTS DISTRIBUTION (STRICT MONOCHROME)")

        if active_contestants:
            df_chart = pd.DataFrame([
                {"Contestant": c["name"].upper(), "Points": c["points"]}
                for c in sorted(active_contestants, key=lambda x: x["points"], reverse=True)
            ])
            st.bar_chart(df_chart.set_index("Contestant"), color="#ffffff", horizontal=True)
        else:
            render_empty_state("NO ACTIVE CONTESTANTS", "Points chart unavailable.")

    # --------------------------------------------------------------------------
    # TAB 3: EVICTION REGISTRY
    # --------------------------------------------------------------------------
    with tab_evict:
        st.markdown("#### EVICTION SYSTEM")
        st.markdown("Permanent eviction protocol. Contestant is removed from all active house systems.")

        active_contestants = get_active_contestants()
        evicted_contestants = get_evicted_contestants()

        col_ev_action, col_ev_list = st.columns([0.45, 0.55])

        with col_ev_action:
            st.markdown("##### EXECUTE EVICTION")
            if not active_contestants:
                st.info("No active contestants available to evict.")
            else:
                ev_options = [c["name"] for c in active_contestants]
                selected_ev = st.selectbox("Select Contestant to Evict", ev_options, key="ctrl_select_ev_c")
                ev_target = get_contestant_by_name(selected_ev)

                if ev_target:
                    st.markdown(
                        f"""
                        <div style="background-color: #111111; border: 1px solid #ffffff; border-radius: 4px; padding: 1rem; margin-bottom: 1rem;">
                            <div style="font-weight: 800; color: #ffffff;">CONFIRM EVICTION: {ev_target['name'].upper()}</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #aaaaaa; margin-top: 0.5rem; line-height: 1.7;">
                                FINAL POINTS: <strong>{ev_target['points']} PTS</strong><br>
                                This will remove the contestant from:<br>
                                &bull; Active House Roster<br>
                                &bull; Leaderboard<br>
                                &bull; Future Nominations<br>
                                &bull; Active Task Assignments<br>
                                &bull; Captaincy
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    ev_reason = st.text_input("Eviction Citation", value="Public Elimination Vote", key="ctrl_ev_reason_input")

                    col_cancel, col_confirm = st.columns(2)
                    with col_cancel:
                        if st.button("CANCEL", use_container_width=True, key="cancel_evict_btn"):
                            trigger_toast("Action cancelled.")
                            st.rerun()
                    with col_confirm:
                        if st.button(f"CONFIRM EVICTION", key="do_evict_btn_ctrl", use_container_width=True):
                            ok, msg = evict_contestant(ev_target["id"], ev_reason)
                            if ok:
                                trigger_toast(f"✓ {ev_target['name']} evicted")
                                st.rerun()
                            else:
                                st.error(msg)

        with col_ev_list:
            st.markdown("##### EVICTED CONTESTANTS REGISTRY")
            if evicted_contestants:
                for ev in evicted_contestants:
                    st.markdown(
                        f"""
                        <div style="background-color: #111111; border: 1px solid #222222; border-radius: 4px; padding: 0.85rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #555555;">EVICTED AT: {ev.get('evicted_time', 'Earlier')}</span>
                                <div style="font-size: 1.05rem; font-weight: 700; color: #777777; text-decoration: line-through;">{ev['name'].upper()}</div>
                                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #555555;">CITATION: {ev.get('eviction_reason', 'Official Eviction')}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; font-weight: 700; color: #666666;">{ev['points']} PTS</div>
                                <span class="badge-evicted">&#10005; EVICTED</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                render_empty_state("NO EVICTIONS RECORDED", "All original housemates remain active in the house.")

    # --------------------------------------------------------------------------
    # TAB 4: FULL ACTIVITY LEDGER
    # --------------------------------------------------------------------------
    with tab_log:
        st.markdown("#### AUDITED REAL-TIME ACTIVITY LEDGER")
        st.markdown("Immutable chronological audit log of all system events, point transactions, challenges, and roster alterations.")

        activities = st.session_state.get("activity_log", [])

        filter_types = ["ALL", "SYSTEM", "POINTS", "TASK", "CAPTAINCY", "NOMINATION", "IMMUNITY", "EVICTION", "ANNOUNCEMENT"]
        selected_type = st.selectbox("FILTER LEDGER BY CATEGORY", filter_types, index=0)

        filtered_logs = activities
        if selected_type != "ALL":
            filtered_logs = [a for a in activities if a.get("type") == selected_type]

        if filtered_logs:
            st.markdown('<div class="bb-card" style="padding: 0.5rem 0.75rem;">', unsafe_allow_html=True)
            for item in filtered_logs:
                st.markdown(
                    f"""
                    <div class="bb-feed-item">
                        <span class="bb-feed-time">{item['time']}</span>
                        <span class="bb-feed-type">{item['type']}</span>
                        <span class="bb-feed-text">{item['text']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            render_empty_state("NO MATCHING ACTIVITY", f"No events recorded in category '{selected_type}'.")

# End of animated page container
st.markdown("</div>", unsafe_allow_html=True)
