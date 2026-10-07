from datetime import datetime
import streamlit as st
from utils.state import add_activity_log

def get_all_contestants():
    return st.session_state.get("contestants", [])

def get_active_contestants():
    return [c for c in get_all_contestants() if not c.get("evicted", False)]

def get_evicted_contestants():
    return [c for c in get_all_contestants() if c.get("evicted", False)]

def get_contestant_by_id(cid):
    for c in get_all_contestants():
        if c["id"] == cid:
            return c
    return None

def get_contestant_by_name(name):
    for c in get_all_contestants():
        if c["name"] == name:
            return c
    return None

def get_current_captain():
    for c in get_active_contestants():
        if c.get("is_captain", False):
            return c
    return None

def set_captain(contestant_id):
    """
    Assign a new House Captain.
    Ensures only ONE contestant can be captain at a time.
    Prevents evicted contestants from becoming captain.
    """
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if target.get("evicted", False):
        return False, f"Cannot make {target['name']} captain: Contestant has been evicted."
    
    current_cap = get_current_captain()
    if current_cap and current_cap["id"] == contestant_id:
        return True, f"{target['name']} is already House Captain."
    
    # Demote previous captain
    if current_cap:
        current_cap["is_captain"] = False
        if current_cap.get("is_immune", False):
            current_cap["status"] = "IMMUNE"
        elif current_cap.get("is_nominated", False):
            current_cap["status"] = "NOMINATED"
        else:
            current_cap["status"] = "ACTIVE"
        prev_name = current_cap["name"]
    else:
        prev_name = "None"
        
    # Promote new captain
    target["is_captain"] = True
    target["status"] = "CAPTAIN"
    
    add_activity_log(
        f"{target['name']} replaced {prev_name} as House Captain.",
        log_type="CAPTAINCY"
    )
    return True, f"{target['name']} is now House Captain."

def adjust_points(contestant_id, points_delta, reason="Manual adjustment"):
    """
    Add or deduct points for a contestant.
    Prevents evicted contestants from receiving points.
    Enforces minimum 0 points.
    """
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if target.get("evicted", False):
        return False, f"Cannot modify points: {target['name']} is evicted."
    
    old_points = target.get("points", 0)
    new_points = max(0, old_points + points_delta)
    actual_delta = new_points - old_points
    target["points"] = new_points
    
    sign = "+" if actual_delta >= 0 else ""
    log_text = f"{target['name']} received {sign}{actual_delta} points. Reason: {reason} (Total: {new_points})"
    add_activity_log(log_text, log_type="POINTS")
    return True, f"Updated {target['name']}'s points to {new_points} ({sign}{actual_delta})."

def nominate_contestant(contestant_id, reason="Big Boss discretion"):
    """
    Nominate an active contestant for eviction.
    RULE: Immune contestants CANNOT be nominated.
    RULE: Evicted contestants CANNOT be nominated.
    RULE: Cannot nominate twice.
    """
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if target.get("evicted", False):
        return False, f"Cannot nominate {target['name']}: Contestant is already evicted."
    if target.get("is_immune", False):
        return False, f"Cannot nominate {target['name']}: Contestant currently holds IMMUNITY."
    if target.get("is_nominated", False):
        return False, f"{target['name']} is already in the Danger Zone."
    
    now_str = datetime.now().strftime("%I:%M %p")
    target["is_nominated"] = True
    target["nomination_reason"] = reason if reason else "Nominated by Big Boss"
    target["nomination_time"] = now_str
    
    if not target.get("is_captain", False):
        target["status"] = "NOMINATED"
        
    add_activity_log(
        f"{target['name']} was nominated for eviction. Reason: {reason}",
        log_type="NOMINATION"
    )
    return True, f"{target['name']} has been nominated and moved to Danger Zone."

def revoke_nomination(contestant_id, reason="Revoked by Big Boss"):
    """Revoke a contestant's nomination."""
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if not target.get("is_nominated", False):
        return False, f"{target['name']} is not nominated."
    
    target["is_nominated"] = False
    target["nomination_reason"] = None
    target["nomination_time"] = None
    
    if target.get("is_captain", False):
        target["status"] = "CAPTAIN"
    elif target.get("is_immune", False):
        target["status"] = "IMMUNE"
    else:
        target["status"] = "ACTIVE"
        
    add_activity_log(
        f"Nomination revoked for {target['name']}. Reason: {reason}",
        log_type="NOMINATION"
    )
    return True, f"Nomination revoked for {target['name']}."

def grant_immunity(contestant_id, reason="Granted by Big Boss"):
    """
    Grant immunity to an active contestant.
    RULE: If contestant was nominated, clears their nomination immediately.
    RULE: Evicted contestants cannot receive immunity.
    """
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if target.get("evicted", False):
        return False, f"Cannot grant immunity: {target['name']} has been evicted."
    
    target["is_immune"] = True
    
    # If currently nominated, clear nomination
    was_nominated = target.get("is_nominated", False)
    if was_nominated:
        target["is_nominated"] = False
        target["nomination_reason"] = None
        target["nomination_time"] = None
    
    if target.get("is_captain", False):
        target["status"] = "CAPTAIN"
    else:
        target["status"] = "IMMUNE"
        
    note = f" (Cleared nomination)" if was_nominated else ""
    add_activity_log(
        f"{target['name']} was granted House Immunity{note}. Reason: {reason}",
        log_type="IMMUNITY"
    )
    return True, f"Immunity granted to {target['name']}.{note}"

def remove_immunity(contestant_id):
    """Remove immunity from a contestant."""
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if not target.get("is_immune", False):
        return False, f"{target['name']} does not have immunity."
    
    target["is_immune"] = False
    
    if target.get("is_captain", False):
        target["status"] = "CAPTAIN"
    elif target.get("is_nominated", False):
        target["status"] = "NOMINATED"
    else:
        target["status"] = "ACTIVE"
        
    add_activity_log(f"Immunity stripped from {target['name']}.", log_type="IMMUNITY")
    return True, f"Immunity removed from {target['name']}."

def evict_contestant(contestant_id, reason="Official Big Boss Eviction"):
    """
    Evict a contestant from the Big Boss House.
    Strictly removes them from:
    - Active house
    - Leaderboard
    - Future nominations
    - Captaincy
    """
    target = get_contestant_by_id(contestant_id)
    if not target:
        return False, "Contestant not found."
    if target.get("evicted", False):
        return False, f"{target['name']} is already evicted."
    
    now_str = datetime.now().strftime("%I:%M %p")
    
    # Clear captaincy if captain
    was_captain = target.get("is_captain", False)
    target["is_captain"] = False
    target["is_nominated"] = False
    target["is_immune"] = False
    target["evicted"] = True
    target["status"] = "EVICTED"
    target["evicted_time"] = now_str
    target["eviction_reason"] = reason
    
    add_activity_log(
        f"{target['name']} has been EVICTED from the House. Final Points: {target.get('points', 0)}.",
        log_type="EVICTION"
    )
    
    # If was captain, log that house has no captain
    if was_captain:
        add_activity_log("House Captain was evicted. Big Boss must appoint a new Captain.", log_type="CAPTAINCY")
        
    return True, f"{target['name']} has been evicted from the House."
