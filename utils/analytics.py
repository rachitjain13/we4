"""
BIG BOSS — HOUSE COMMAND CENTER
Performance Analytics Computation Engine
Calculates analytical metrics purely from current real application state.
"""

import pandas as pd
import streamlit as st
from utils.contestants import get_all_contestants, get_active_contestants, get_current_captain
from utils.tasks import get_all_tasks
from utils.questions import get_all_questions

def get_analytics_summary():
    """Top summary KPIs calculated from live state."""
    active_contestants = get_active_contestants()
    all_tasks = get_all_tasks()
    all_questions = get_all_questions()

    total_active = len(active_contestants)
    total_pts = sum(c.get("points", 0) for c in active_contestants)
    avg_pts = round(total_pts / total_active, 1) if total_active > 0 else 0

    tasks_completed = len([t for t in all_tasks if t.get("status") == "COMPLETED"])
    tasks_pending = len([t for t in all_tasks if t.get("status") == "PENDING"])
    
    total_nominees = len([c for c in active_contestants if c.get("is_nominated", False)])
    immune_count = len([c for c in active_contestants if c.get("is_immune", False)])
    questions_solved = len([q for q in all_questions if q.get("solved", False)])

    return {
        "active_contestants": total_active,
        "total_points": total_pts,
        "average_points": avg_pts,
        "tasks_completed": tasks_completed,
        "tasks_pending": tasks_pending,
        "total_nominees": total_nominees,
        "immune_contestants": immune_count,
        "questions_solved": questions_solved
    }

def get_contestant_questions_solved_map():
    """Map contestant name to number of questions solved."""
    all_q = get_all_questions()
    q_map = {}
    for q in all_q:
        if q.get("solved") and q.get("solved_by"):
            solver = q["solved_by"].upper()
            q_map[solver] = q_map.get(solver, 0) + 1
    return q_map

def calculate_performance_score(contestant, max_pts, max_tasks, max_questions):
    """
    Transparent Performance Score (0 - 100):
    - 50% Points Contribution: (points / max_house_points) * 50
    - 30% Task Completion Contribution: (tasks_completed / max_tasks) * 30
    - 20% Challenge Contribution: (questions_solved / max_questions) * 20
    - Nomination Pressure Penalty: -10 if nominated
    Bounded between 0 and 100.
    """
    pts = contestant.get("points", 0)
    pts_comp = (pts / max_pts * 50) if max_pts > 0 else 0

    tasks_done = contestant.get("tasks_completed", 0)
    task_comp = (tasks_done / max_tasks * 30) if max_tasks > 0 else 0

    q_map = get_contestant_questions_solved_map()
    q_done = q_map.get(contestant["name"].upper(), 0)
    q_comp = (q_done / max_questions * 20) if max_questions > 0 else 0

    nom_penalty = 10 if contestant.get("is_nominated", False) else 0

    raw_score = pts_comp + task_comp + q_comp - nom_penalty
    return round(max(0.0, min(100.0, raw_score)), 1)

def get_contestant_performance_data(team_filter="ALL", status_filter="ALL"):
    """
    Compile contestant performance dataset from live state.
    Excludes evicted contestants from rankings unless explicitly filtered.
    """
    all_c = get_all_contestants()
    active_c = get_active_contestants()
    q_map = get_contestant_questions_solved_map()

    # Determine maximums for normalization
    max_pts = max([c.get("points", 0) for c in active_c], default=1)
    max_tasks = max([c.get("tasks_completed", 0) for c in active_c], default=1)
    max_q = max(list(q_map.values()), default=1)

    # Sort all by points descending
    sorted_all = sorted(all_c, key=lambda x: x.get("points", 0), reverse=True)

    records = []
    active_rank = 1

    for c in sorted_all:
        is_evicted = c.get("evicted", False)
        
        # Filtering logic
        if team_filter != "ALL" and c.get("team", "").upper() != team_filter.upper():
            continue
        if status_filter == "ACTIVE ONLY" and is_evicted:
            continue
        elif status_filter == "IMMUNE" and (not c.get("is_immune", False) or is_evicted):
            continue
        elif status_filter == "NOMINATED" and (not c.get("is_nominated", False) or is_evicted):
            continue
        elif status_filter == "CAPTAIN" and not c.get("is_captain", False):
            continue
        elif status_filter == "EVICTED" and not is_evicted:
            continue

        rank_display = f"#{active_rank:02d}" if not is_evicted else "—"
        if not is_evicted:
            active_rank += 1

        perf_score = calculate_performance_score(c, max_pts, max_tasks, max_q) if not is_evicted else 0.0
        q_count = q_map.get(c["name"].upper(), 0)

        status_str = "EVICTED" if is_evicted else (
            "CAPTAIN" if c.get("is_captain") else (
                "IMMUNE" if c.get("is_immune") else (
                    "NOMINATED" if c.get("is_nominated") else "ACTIVE"
                )
            )
        )

        records.append({
            "Rank": rank_display,
            "Contestant": c["name"].upper(),
            "Team": c["team"].upper(),
            "Points": c.get("points", 0),
            "Tasks Completed": c.get("tasks_completed", 0),
            "Questions Solved": q_count,
            "Nominated": "YES" if c.get("is_nominated") else "NO",
            "Immune": "YES" if c.get("is_immune") else "NO",
            "Status": status_str,
            "Performance Score": perf_score
        })

    return pd.DataFrame(records) if records else pd.DataFrame()

def get_performance_spotlights():
    """Calculate key analytical spotlight performers from real state."""
    active_c = get_active_contestants()
    if not active_c:
        return {
            "top_performer": "NONE",
            "top_task_performer": "NONE",
            "top_puzzle_performer": "NONE",
            "most_nominated": "NONE",
            "current_captain": "NONE",
            "highest_momentum": "NONE"
        }

    q_map = get_contestant_questions_solved_map()
    
    # 1. Top points performer
    top_pts_c = max(active_c, key=lambda x: x.get("points", 0))
    top_performer = f"{top_pts_c['name'].upper()} ({top_pts_c['team'].upper()}) — {top_pts_c.get('points', 0)} PTS"

    # 2. Top task performer
    top_task_c = max(active_c, key=lambda x: x.get("tasks_completed", 0))
    top_task_performer = f"{top_task_c['name'].upper()} ({top_task_c['team'].upper()}) — {top_task_c.get('tasks_completed', 0)} TASKS"

    # 3. Top puzzle performer
    if q_map:
        top_q_name = max(q_map, key=q_map.get)
        top_puzzle_performer = f"{top_q_name} — {q_map[top_q_name]} SOLVED"
    else:
        top_puzzle_performer = "NONE SOLVED YET"

    # 4. Most nominated (currently in danger zone)
    nominees = [c for c in active_c if c.get("is_nominated", False)]
    if nominees:
        most_nom = f"{', '.join([c['name'].upper() for c in nominees])}"
    else:
        most_nom = "NONE IN DANGER"

    # 5. Current House Captain
    cap = get_current_captain()
    cap_str = f"{cap['name'].upper()} ({cap['team'].upper()})" if cap else "NONE"

    # 6. Highest Momentum / Top Performance Score
    max_pts = max([c.get("points", 0) for c in active_c], default=1)
    max_tasks = max([c.get("tasks_completed", 0) for c in active_c], default=1)
    max_q = max(list(q_map.values()), default=1)
    top_score_c = max(active_c, key=lambda x: calculate_performance_score(x, max_pts, max_tasks, max_q))
    top_score = calculate_performance_score(top_score_c, max_pts, max_tasks, max_q)
    highest_momentum = f"{top_score_c['name'].upper()} — {top_score} / 100"

    return {
        "top_performer": top_performer,
        "top_task_performer": top_task_performer,
        "top_puzzle_performer": top_puzzle_performer,
        "most_nominated": most_nom,
        "current_captain": cap_str,
        "highest_momentum": highest_momentum
    }

def get_team_comparison_analytics():
    """Compare Team Alpha vs Team Beta using live state."""
    active_c = get_active_contestants()
    all_tasks = get_all_tasks()
    q_map = get_contestant_questions_solved_map()

    alpha_members = [c for c in active_c if c.get("team", "").upper() == "ALPHA"]
    beta_members = [c for c in active_c if c.get("team", "").upper() == "BETA"]

    def calc_team(members):
        count = len(members)
        tot_pts = sum(m.get("points", 0) for m in members)
        avg_pts = round(tot_pts / count, 1) if count > 0 else 0
        tasks = sum(m.get("tasks_completed", 0) for m in members)
        noms = len([m for m in members if m.get("is_nominated", False)])
        qs = sum(q_map.get(m["name"].upper(), 0) for m in members)
        return {
            "members": count,
            "total_points": tot_pts,
            "average_points": avg_pts,
            "tasks_completed": tasks,
            "nominations": noms,
            "questions_solved": qs
        }

    return {
        "alpha": calc_team(alpha_members),
        "beta": calc_team(beta_members)
    }
