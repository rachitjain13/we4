"""
BIG BOSS — HOUSE COMMAND CENTER
Questions and Puzzle Challenge Management Module
"""

from datetime import datetime
import streamlit as st
from utils.state import add_activity_log
from utils.alerts import add_alert
from utils.contestants import get_contestant_by_id, adjust_points, get_active_contestants

def get_all_questions():
    """Retrieve all puzzle challenges from session state."""
    return st.session_state.get("questions", [])

def get_question_by_id(qid):
    """Find question by ID."""
    for q in get_all_questions():
        if q["id"] == qid:
            return q
    return None

def check_answer(expected_answer, submitted_answer, case_sensitive=False):
    """Normalize and compare submitted answer with expected answer."""
    if not submitted_answer or not expected_answer:
        return False
    
    sub = submitted_answer.strip()
    exp = expected_answer.strip()
    
    if not case_sensitive:
        return sub.lower() == exp.lower()
    return sub == exp

def submit_answer(question_id, contestant_id, submitted_answer):
    """
    Evaluate contestant's answer submission.
    
    Rules enforced:
    1. Only active contestants can answer.
    2. Evicted contestants cannot answer.
    3. Solved questions cannot be solved again.
    4. Correct answer awards points to contestant, updates leaderboard & activity log.
    5. Incorrect answer records log without revealing expected answer.
    """
    q = get_question_by_id(question_id)
    if not q:
        return False, "Question not found.", 0
    
    if q.get("solved", False):
        return False, f"This challenge has already been solved by {q.get('solved_by', 'another contestant')}.", 0
    
    contestant = get_contestant_by_id(contestant_id)
    if not contestant:
        return False, "Selected contestant not found.", 0
    
    if contestant.get("evicted", False):
        return False, f"Cannot submit: {contestant['name']} has been evicted from the House.", 0
    
    if not submitted_answer or not submitted_answer.strip():
        return False, "Submission cannot be blank.", 0
        
    is_correct = check_answer(
        expected_answer=q.get("answer", ""),
        submitted_answer=submitted_answer,
        case_sensitive=q.get("case_sensitive", False)
    )
    
    now_str = datetime.now().strftime("%I:%M %p")
    q_title = q.get("title", f"Question {q['id']}")
    
    if is_correct:
        pts = q.get("points", 500)
        q["solved"] = True
        q["solved_by"] = contestant["name"].upper()
        q["solved_at"] = now_str
        
        # Award points to contestant directly via core points system
        adjust_points(
            contestant_id=contestant["id"],
            points_delta=pts,
            reason=f"Solved {q_title} challenge"
        )
        
        add_activity_log(
            f"{contestant['name'].upper()} solved {q_title} (+{pts} PTS).",
            log_type="QUESTION"
        )
        add_alert(
            "SUCCESS",
            "Puzzle Solved",
            f"{contestant['name'].upper()} ({contestant['team'].upper()}) solved {q_title} and earned +{pts} points.",
            priority="MEDIUM",
            related_contestant=contestant['name'],
            related_question=q_title
        )
        
        return True, f"CORRECT ANSWER! +{pts} POINTS awarded to {contestant['name'].upper()}.", pts
    else:
        # Incorrect answer - do not reveal the answer
        add_activity_log(
            f"{contestant['name'].upper()} submitted an incorrect answer for {q_title}.",
            log_type="QUESTION"
        )
        return False, "INCORRECT ANSWER. Try again.", 0

def create_question(title, qtype, content, answer, points, max_points, hint=None, case_sensitive=False, image_path=None):
    """Create a new challenge question."""
    if not content or not content.strip():
        return False, "Question content cannot be empty."
    if not answer or not answer.strip():
        return False, "Answer cannot be empty."
        
    questions = st.session_state.get("questions", [])
    new_id = f"q-{len(questions) + 1:02d}"
    
    new_q = {
        "id": new_id,
        "title": title.strip() if title else f"Q{len(questions) + 1}",
        "type": qtype.lower(),
        "content": content.strip(),
        "hint": hint.strip() if hint else "",
        "answer": answer.strip(),
        "points": int(points),
        "max_points": int(max_points),
        "case_sensitive": bool(case_sensitive),
        "image_path": image_path.strip() if image_path else None,
        "solved": False,
        "solved_by": None,
        "solved_at": None
    }
    
    questions.append(new_q)
    add_activity_log(f"New challenge question created: {new_q['title']} (+{points} pts).", log_type="QUESTION")
    return True, f"Challenge {new_q['title']} created successfully."

def reset_question(question_id):
    """
    Reset a question to unsolved state.
    Does not revoke previously awarded points (per Rule 10).
    """
    q = get_question_by_id(question_id)
    if not q:
        return False, "Question not found."
    
    q["solved"] = False
    q["solved_by"] = None
    q["solved_at"] = None
    add_activity_log(f"Question {q.get('title', q['id'])} was reset to unsolved state.", log_type="QUESTION")
    return True, f"Question {q.get('title', q['id'])} reset to unsolved."

def delete_question(question_id):
    """Delete a question without corrupting contestant points."""
    questions = st.session_state.get("questions", [])
    target = get_question_by_id(question_id)
    if not target:
        return False, "Question not found."
        
    st.session_state.questions = [q for q in questions if q["id"] != question_id]
    add_activity_log(f"Question {target.get('title', target['id'])} was deleted.", log_type="QUESTION")
    return True, f"Question {target.get('title', target['id'])} removed."

def get_question_stats():
    """Compute live statistics for puzzle challenges."""
    questions = get_all_questions()
    total = len(questions)
    solved = len([q for q in questions if q.get("solved", False)])
    remaining = total - solved
    total_pts_awarded = sum(q.get("points", 0) for q in questions if q.get("solved", False))
    
    # Calculate top solver
    solver_counts = {}
    for q in questions:
        if q.get("solved") and q.get("solved_by"):
            solver = q["solved_by"]
            solver_counts[solver] = solver_counts.get(solver, 0) + 1
            
    top_solver = "NONE"
    if solver_counts:
        top_solver = max(solver_counts, key=solver_counts.get)
        
    return {
        "total": total,
        "solved": solved,
        "remaining": remaining,
        "points_awarded": total_pts_awarded,
        "top_solver": top_solver
    }
