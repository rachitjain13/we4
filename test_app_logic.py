import streamlit as st
from utils.state import init_session_state, broadcast_announcement, add_activity_log
from utils.contestants import (
    get_all_contestants, get_active_contestants, get_evicted_contestants,
    get_contestant_by_name, set_captain, adjust_points, nominate_contestant,
    revoke_nomination, grant_immunity, remove_immunity, evict_contestant, get_current_captain
)
from utils.tasks import get_all_tasks, create_task, start_task, complete_task, delete_task
from utils.questions import (
    get_all_questions, get_question_by_id, submit_answer,
    create_question, reset_question, delete_question, get_question_stats
)

def run_tests():
    init_session_state()

    # 1. Test initial data
    contestants = get_all_contestants()
    assert len(contestants) == 10, f"Expected 10 contestants, got {len(contestants)}"
    aarav = get_contestant_by_name("Aarav")
    assert aarav["is_immune"] == True, "Aarav should be immune"
    rahul = get_contestant_by_name("Rahul")
    assert rahul["is_captain"] == True, "Rahul should be captain"
    print("Test 1 Passed: Initial data verified.")

    # 2. Test Point System & non-negative rule
    adjust_points(aarav["id"], 50, "Challenge won")
    assert aarav["points"] == 920, f"Expected 920, got {aarav['points']}"
    adjust_points(aarav["id"], -1000, "Huge penalty")
    assert aarav["points"] == 0, "Points should not go below 0"
    adjust_points(aarav["id"], 870, "Reset")
    print("Test 2 Passed: Point system & floor at 0 verified.")

    # 3. Test Captaincy - only 1 captain
    set_captain(aarav["id"])
    assert aarav["is_captain"] == True
    assert rahul["is_captain"] == False
    assert get_current_captain()["id"] == aarav["id"]
    print("Test 3 Passed: Captaincy change verified.")

    # 4. Test Nomination Rules - Immune cannot be nominated
    ok, msg = nominate_contestant(aarav["id"], "Test reason")
    assert not ok, "Aarav is immune, should NOT be nominatable"
    assert "IMMUNITY" in msg or "IMMUNE" in msg

    kabir = get_contestant_by_name("Kabir")
    ok, msg = nominate_contestant(kabir["id"], "Poor performance")
    assert ok, "Kabir should be nominated"
    assert kabir["is_nominated"] == True

    # Duplicate nomination prevented
    ok2, msg2 = nominate_contestant(kabir["id"], "Again")
    assert not ok2, "Should not allow duplicate nomination"
    print("Test 4 Passed: Nomination rules & immunity protection verified.")

    # 5. Test Immunity clearing nomination
    grant_immunity(kabir["id"])
    assert kabir["is_immune"] == True
    assert kabir["is_nominated"] == False, "Granting immunity should clear nomination"
    print("Test 5 Passed: Immunity and nomination clearing verified.")

    # 6. Test Tasks - Auto points award
    create_task("Test Cleanup", "Desc", "TEAM", "Team Beta", 100, 30, "Today")
    new_t = get_all_tasks()[0]
    assert new_t["status"] == "PENDING"
    start_task(new_t["id"])
    assert new_t["status"] == "IN PROGRESS"

    riya = get_contestant_by_name("Riya") # Beta
    riya_pts_before = riya["points"]
    complete_task(new_t["id"])
    assert new_t["status"] == "COMPLETED"
    assert riya["points"] == riya_pts_before + 100, "Team Beta members should get +100"

    # Cannot complete twice
    ok_c, msg_c = complete_task(new_t["id"])
    assert not ok_c, "Cannot complete twice"
    print("Test 6 Passed: Task execution & points auto-disbursement verified.")

    # 7. Test Eviction
    nisha = get_contestant_by_name("Nisha")
    evict_contestant(nisha["id"], "Public vote")
    assert nisha["evicted"] == True
    assert nisha not in get_active_contestants()
    assert nisha in get_evicted_contestants()

    # Evicted cannot receive points or nominations
    ok_p, _ = adjust_points(nisha["id"], 100)
    assert not ok_p, "Evicted cannot receive points"
    ok_n, _ = nominate_contestant(nisha["id"])
    assert not ok_n, "Evicted cannot be nominated"
    print("Test 7 Passed: Eviction restrictions strictly verified.")

    # 8. Test Announcements
    broadcast_announcement("Test broadcast", "Critical")
    assert st.session_state.current_announcement["message"] == "Test broadcast"
    print("Test 8 Passed: Announcement system verified.")

    # 9. Test Questions Module - Initial Questions Loaded
    questions = get_all_questions()
    assert len(questions) >= 5, f"Expected at least 5 questions, got {len(questions)}"
    q1 = get_question_by_id("q-01")
    assert q1 is not None, "q-01 should exist"
    assert q1["type"] == "hex"
    print("Test 9 Passed: Questions loaded with multiple puzzle types.")

    # 10. Test Questions - Incorrect Answer
    meera = get_contestant_by_name("Meera")
    meera_pts_before = meera["points"]
    ok_wrong, msg_wrong, pts_wrong = submit_answer("q-01", meera["id"], "wrong_answer_xyz")
    assert not ok_wrong, "Wrong answer should fail"
    assert pts_wrong == 0, "No points should be awarded for wrong answer"
    assert meera["points"] == meera_pts_before, "Points should remain unchanged"
    assert not q1["solved"], "Question should remain unsolved"
    print("Test 10 Passed: Incorrect answer rejection verified.")

    # 11. Test Questions - Correct Answer & Leaderboard update
    ok_correct, msg_correct, pts_awarded = submit_answer("q-01", meera["id"], "solaris")
    assert ok_correct, "Expected 'solaris' to be correct"
    assert pts_awarded == 500, f"Expected 500 points, got {pts_awarded}"
    assert meera["points"] == meera_pts_before + 500, "Meera should receive +500 points"
    assert q1["solved"] == True, "q-01 should now be marked solved"
    assert q1["solved_by"] == meera["name"].upper()

    # Cannot solve twice
    ok_again, msg_again, _ = submit_answer("q-01", meera["id"], "solaris")
    assert not ok_again, "Cannot solve already-solved question"
    print("Test 11 Passed: Correct answer scoring and double-submission guard verified.")

    # 12. Test Questions - Evicted contestant restriction & stats
    ok_ev_ans, msg_ev_ans, _ = submit_answer("q-02", nisha["id"], "antigravity")
    assert not ok_ev_ans, "Evicted contestant (Nisha) must NOT be able to solve questions"
    
    q_stats = get_question_stats()
    assert q_stats["solved"] >= 1, "At least 1 question should be counted as solved"
    assert q_stats["top_solver"] == meera["name"].upper(), f"Expected top solver Meera, got {q_stats['top_solver']}"
    
    # Test reset & delete question
    reset_question("q-01")
    assert not q1["solved"], "Reset question should be unsolved"
    assert meera["points"] == meera_pts_before + 500, "Points should remain intact upon reset per Rule 10"
    print("Test 12 Passed: Evicted solver restriction, stats & reset safety verified.")

    # 13. Test Live Alert Engine
    from utils.alerts import (
        get_all_alerts, get_unread_alerts, get_unread_alerts_count,
        add_alert, mark_alert_read, mark_all_alerts_read, clear_old_alerts
    )
    alerts = get_all_alerts()
    assert len(alerts) > 0, "Alerts should have been generated by prior contestant & task actions"
    initial_unread = get_unread_alerts_count()
    assert initial_unread > 0, "There should be unread alerts"

    # Add alert & deduplication check
    new_a = add_alert("WARNING", "Perimeter Breach", "Surveillance camera 4 offline", "HIGH")
    assert new_a["title"] == "Perimeter Breach"
    count_after = len(get_all_alerts())
    # Duplicate alert call
    dup_a = add_alert("WARNING", "Perimeter Breach", "Surveillance camera 4 offline", "HIGH")
    assert len(get_all_alerts()) == count_after, "Duplicate identical alert should not be re-added"

    # Mark specific alert read
    ok_mr = mark_alert_read(new_a["id"])
    assert ok_mr, "Alert should be marked as read"
    assert new_a["read"] == True

    # Mark all alerts read
    mark_all_alerts_read()
    assert get_unread_alerts_count() == 0, "Unread alerts count should be 0 after mark_all_alerts_read"

    # Clear old read alerts
    clear_old_alerts()
    assert len(get_unread_alerts()) == 0
    print("Test 13 Passed: Alert engine (creation, deduplication, read tracking, clear) verified.")

    # 14. Test Performance Analytics Engine
    from utils.analytics import (
        get_analytics_summary, get_contestant_performance_data,
        get_performance_spotlights, get_team_comparison_analytics,
        calculate_performance_score
    )
    summary = get_analytics_summary()
    assert summary["active_contestants"] == len(get_active_contestants())
    assert summary["total_points"] == sum(c["points"] for c in get_active_contestants())
    assert summary["average_points"] > 0
    assert summary["tasks_completed"] >= 1

    # Audit DataFrame
    df_perf = get_contestant_performance_data()
    assert not df_perf.empty, "Performance dataframe should not be empty"
    expected_cols = ["Rank", "Contestant", "Team", "Points", "Tasks Completed", "Questions Solved", "Nominated", "Immune", "Status", "Performance Score"]
    for col in expected_cols:
        assert col in df_perf.columns, f"Missing column {col} in analytics dataframe"

    # Performance Score bounds
    sample_c = get_active_contestants()[0]
    score = calculate_performance_score(sample_c, 2000, 10, 5)
    assert 0.0 <= score <= 100.0, f"Score {score} out of bounds [0, 100]"

    # Spotlights & Team Breakdown
    spotlights = get_performance_spotlights()
    assert "top_performer" in spotlights
    assert "top_task_performer" in spotlights
    assert "highest_momentum" in spotlights

    teams = get_team_comparison_analytics()
    assert "alpha" in teams and "beta" in teams
    assert teams["alpha"]["members"] + teams["beta"]["members"] == len(get_active_contestants())
    assert teams["alpha"]["total_points"] >= 0
    print("Test 14 Passed: Performance analytics (KPIs, scoring, spotlights, faction comparison) verified.")

    print("\n=================================================================")
    print("ALL 12 CORE RULES + QUESTIONS PUZZLE + ANALYTICS + ALERTS PASSED!")
    print("=================================================================")

if __name__ == "__main__":
    run_tests()

