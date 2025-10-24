# Gesture-and-Voice-Controlled-Personal-Assistant

Hybrid (Dispatcher + DB)

This is the architecture you’re aiming for — dynamic, persistent, and GUI-friendly.

1. Database structure

modes table → stores available modes (e.g. "daily", "wuthering waves")

actions table → stores commands per mode ("mute" → mute())

global_actions table → stores commands valid in any mode

2. Dispatcher in memory

At runtime you build dispatcher from DB rows:

For each global action → dispatcher["mute"] = mute

For each mode action → dispatcher[f"{mode}:{command}"] = func

For each mode → dispatcher["change to {mode}"] = lambda: set_mode(mode)

This makes dispatcher the “fast lookup table” for execution.

3. Intent resolution

Speech recognition returns text → "mute" or "change to daily mode"

rule_based_intent checks:

If the phrase is in dispatcher, return it as an "action"

If the phrase is "change to …", also recognized by dispatcher → triggers set_mode()

Result: handler only ever calls execute_action(command).

4. Execution

execute_action looks up the command in dispatcher and calls the function.

5. GUI integration

GUI adds a mode → inserts into modes table, triggers dispatcher reload.

GUI adds an action → inserts into actions or global_actions, reloads dispatcher.

GUI deletes an action/mode → removes from DB, reloads dispatcher.

6. Persistence

All changes are stored in DB.

On restart, you reload dispatcher from DB → nothing is lost.

🔹 End product (Option 4)

Voice layer (Vosk) → recognizes commands only from known_phrases generated from DB.

Intent layer (rule_based_intent) → simply checks dispatcher (no messy string slicing).

Execution layer (execute_action) → looks up dispatcher and runs function.

DB layer (SQLite) → permanent source of truth for modes + actions.

GUI layer → lets you add/remove/edit modes and actions at runtime, which updates DB and refreshes dispatcher.

✅ The benefit:

One uniform dispatcher: both mode switching and commands go through the same system.

Runtime editable: add/remove modes or commands without restarting.

Persistent: DB stores everything, so GUI changes survive restarts.

Clean code: rule_based_intent becomes “if it’s in dispatcher, return it” — no special cases.