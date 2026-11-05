#!/bin/bash
# Description: Launches the V3 Pipeline Agent on the remote PVE server inside Zellij.

PVE_HOST="Antigravity"
PROJECT_DIR="~/Projects/psy_garden" 
SESSION="Antiverse"
TAB_NAME="[psy_garden] Pipeline"
PROMPT_FILE="/Users/kael/.gemini/Projects/psy_garden/commands/pipeline_prompt.md"
REMOTE_PROMPT_FILE="/tmp/pipeline_prompt.md"

echo "Syncing prompt file to PVE..."
scp "$PROMPT_FILE" "$PVE_HOST:$REMOTE_PROMPT_FILE"

echo "Creating loop wrapper script on PVE..."
ssh $PVE_HOST "cat << 'EOF' > /tmp/run_pipeline.sh
#!/bin/bash
cd $PROJECT_DIR
while true; do
    echo \"[Pipeline] Waking up Agent...\"
    echo \"0\" > /tmp/sleep_time.txt
    agy --remote-control --dangerously-skip-permissions --model gemini-3.8-flash --effort low --prompt \"\$(cat $REMOTE_PROMPT_FILE)\"
    
    SLEEP_VAL=\$(cat /tmp/sleep_time.txt)
    if [ \"\$SLEEP_VAL\" == \"DONE\" ]; then
        echo \"[Pipeline] All 386 plants completed! Exiting loop.\"
        break
    elif [[ \"\$SLEEP_VAL\" =~ ^[0-9]+$ ]] && [ \"\$SLEEP_VAL\" -gt 0 ]; then
        echo \"[Pipeline] Quota Exhausted! Sleeping for \$SLEEP_VAL seconds...\"
        sleep \$SLEEP_VAL
    else
        echo \"[Pipeline] Batch finished. Waiting 5s before next batch...\"
        sleep 5
    fi
done
EOF
chmod +x /tmp/run_pipeline.sh"

echo "Spawning V3 Pipeline Agent on PVE ($PVE_HOST)..."
ssh $PVE_HOST "zellij --session $SESSION action new-tab --name '$TAB_NAME' && \
sleep 2 && \
zellij --session $SESSION action write-chars 'bash /tmp/run_pipeline.sh' && \
zellij --session $SESSION action send-keys 'Enter'"

echo "============================================="
echo "✅ Pipeline successfully launched in Zellij tab: $TAB_NAME"
echo "============================================="
