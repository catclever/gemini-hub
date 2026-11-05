#!/usr/bin/env bash
# ==============================================================================
# pve_watchdog.sh: Local Mac Dispatcher & Watchdog for PVE Antigravity Tasks
# ==============================================================================
# Architecture:
#   1. Runs LOCALLY on Mac. Never executes as a PVE-internal tab process.
#   2. Injects pure Antigravity (agy -i) directly into PVE's Antiverse session.
#   3. The remote Zellij tab is 100% Antigravity TUI — zero watchdog wrapper noise.
#   4. The watchdog loop stays on Mac, polling task completion signals via SSH.
# ==============================================================================

set -eo pipefail

AGENT_TYPE="dev"
MODEL=""
EFFORT=""
TIER=""
TASK_ID=""
PROJECT_DIR=""
PROMPT=""

WARM_HOURS=2

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--task) TASK_ID="$2"; shift 2 ;;
        -a|--agent) AGENT_TYPE="$2"; shift 2 ;;
        -d|--dir) PROJECT_DIR="$2"; shift 2 ;;
        -p|--prompt) PROMPT="$2"; shift 2 ;;
        -m|--model) MODEL="$2"; shift 2 ;;
        --effort) EFFORT="$2"; shift 2 ;;
        --tier) TIER="$2"; shift 2 ;;
        --warm-hours) WARM_HOURS="$2"; shift 2 ;;
        *) echo "Unknown parameter passed: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$TASK_ID" || -z "$PROJECT_DIR" || -z "$PROMPT" ]]; then
    echo "Usage: $0 -t <Task_ID> -a <dev|ops> -d <Project_Dir> -p <Prompt> [--tier <dev|ops|pro>] [-m <model>] [--effort <low|medium|high>]" >&2
    exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_DIR")

# Determine default tier if not explicitly specified
if [[ -z "$TIER" ]]; then
    if [[ "$AGENT_TYPE" == "ops" ]]; then
        TIER="ops"
    else
        TIER="dev"
    fi
fi

# Resolve Tier Settings (Default to flash models to avoid consuming interactive 3.1 Pro)
case "$TIER" in
    pro|max)
        DEFAULT_MODEL="gemini-3.1-pro"
        DEFAULT_EFFORT="high"
        ;;
    ops|fast|middle|medium)
        DEFAULT_MODEL="gemini-3.8-flash"
        DEFAULT_EFFORT="medium"
        ;;
    dev|balanced|standard|*)
        DEFAULT_MODEL="gemini-3.8-flash-high"
        DEFAULT_EFFORT="high"
        ;;
esac

# Allow explicit model override via -m
if [[ -z "$MODEL" ]]; then
    MODEL="$DEFAULT_MODEL"
fi
if [[ -z "$EFFORT" ]]; then
    EFFORT="$DEFAULT_EFFORT"
fi

# Safety clamp for gemini-3.1-pro: Google only supports 'low' and 'high' (no 'medium')
if [[ "$MODEL" == *"3.1-pro"* && "$EFFORT" == "medium" ]]; then
    EFFORT="high"
fi

# Resolve Remote Working Directory and Session Name on PVE
REMOTE_DIR="/root/Projects/${PROJECT_NAME}"
SESSION_NAME="[${PROJECT_NAME}] ${AGENT_TYPE}-${TASK_ID}"

echo "======================================================================"
echo "🐕 [Local Watchdog] Preparing PVE Remote Task: $TASK_ID"
echo "🎯 Agent: $AGENT_TYPE | Tier: $TIER | Model: $MODEL ($EFFORT effort)"
echo "📂 Remote Target: $REMOTE_DIR"
echo "🌌 Dedicated Session: $SESSION_NAME"
echo "======================================================================"

# Base prompt with safety overrides
SAFE_PROMPT="Execute Task ID: ${TASK_ID}. ${PROMPT}. You are STRICTLY FORBIDDEN from updating task metadata files in tasks/. When finished, write DONE to /tmp/${TASK_ID}.signal."

# 1. Clean previous signal and inject prompt cleanly onto PVE disk
ssh Antigravity "rm -f /tmp/${TASK_ID}.signal /tmp/prompt_${TASK_ID}.txt 2>/dev/null || true"
echo "$SAFE_PROMPT" | ssh Antigravity "cat > /tmp/prompt_${TASK_ID}.txt"

# 2. Build agent invocation flag
AGENT_FLAG=""
if [[ "$AGENT_TYPE" == "dev" ]]; then
    AGENT_FLAG="--agent dev"
elif [[ "$AGENT_TYPE" == "ops" ]]; then
    AGENT_FLAG="--agent ops"
fi

# 3. Create runner script on PVE to safely load prompt with explicit model and effort flags
ssh Antigravity "bash -s" << EOF
cat << 'RUNNER_EOF' > /tmp/run_${TASK_ID}.sh
#!/usr/bin/env bash
[ -f /etc/profile ] && source /etc/profile 2>/dev/null || true
[ -f /root/.bashrc ] && source /root/.bashrc 2>/dev/null || true
[ -f /etc/environment ] && export \$(grep -v '^\#' /etc/environment | xargs) 2>/dev/null || true
cd "${REMOTE_DIR}" || exit 1
PROMPT=\$(cat /tmp/prompt_${TASK_ID}.txt)
exec agy --remote-control --dangerously-skip-permissions ${AGENT_FLAG} --model "${MODEL}" --effort "${EFFORT}" -i "\$PROMPT"
RUNNER_EOF
chmod +x /tmp/run_${TASK_ID}.sh
EOF

echo "[Local Watchdog] Spawning Antigravity in dedicated Zellij session '${SESSION_NAME}' (Warm Period: ${WARM_HOURS}h)..."

ssh Antigravity "antiverse-run \
  --name '${SESSION_NAME}' \
  --tier '${TIER}' \
  --warm-hours '${WARM_HOURS}' \
  --cwd '${REMOTE_DIR}' \
  --force \
  -- /tmp/run_${TASK_ID}.sh"

echo "======================================================================"
echo "📺 [Monitor] To view session: ssh Antigravity -t 'antiverse a ${TASK_ID}'"
echo "💡 [Tip] Press [Alt + s] inside any Zellij window to switch tasks instantly."
echo "☕ [Warm Period] Session stays active for ${WARM_HOURS} hours post-completion,"
echo "                 then sleeps into (EXITED) state to save resources."
echo "======================================================================"
echo "[Local Watchdog] Antigravity process launched on PVE. Now watching for completion..."

# 4. Polling loop runs exclusively on local Mac
POLL_COUNT=0
while true; do
    sleep 15
    POLL_COUNT=$((POLL_COUNT + 1))
    
    STATUS=$(ssh -o ConnectTimeout=10 Antigravity "cat /tmp/${TASK_ID}.signal 2>/dev/null" || true)
    
    if [[ "$STATUS" == *"DONE"* ]]; then
        echo ""
        echo "======================================================================"
        echo "🎉 [Local Watchdog] Remote Task $TASK_ID Finished: DONE"
        echo "☕ Session '${SESSION_NAME}' is active in ${WARM_HOURS}-hour warm period."
        echo "👉 Attach anytime: ssh Antigravity -t 'antiverse a ${TASK_ID}'"
        echo "💤 Will automatically sleep into (EXITED) after ${WARM_HOURS}h if unviewed."
        echo "======================================================================"
        exit 0
    elif [[ "$STATUS" == *"FAILED"* ]]; then
        echo ""
        echo "======================================================================"
        echo "❌ [Local Watchdog] Remote Task $TASK_ID Failed: $STATUS"
        echo "======================================================================"
        exit 1
    fi

    # Output periodic heartbeat every minute
    if (( POLL_COUNT % 4 == 0 )); then
        echo "[Local Watchdog] Task $TASK_ID is running on PVE ($((POLL_COUNT * 15))s elapsed)..."
    fi
done
