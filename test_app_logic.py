import streamlit as st
from utils.state import init_session_state, broadcast_announcement, add_activity_log
from utils.contestants import (
    get_all_contestants, get_active_contestants, get_evicted_contestants,
    get_contestant_by_name, set_captain, adjust_points, nominate_contestant,
    revoke_nomination, grant_immunity, remove_immunity, evict_contestant, get_current_captain
)
from utils.tasks import get_all_tasks, create_task, start_task, complete_task, delete_task

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

    print("\n=======================================================")
    print("ALL 12 MANDATORY BUSINESS LOGIC RULES VERIFIED 100% OPERATIONAL!")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
