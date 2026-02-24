#!/bin/bash
# PsyDaily Bot 自动保活脚本
# 每5分钟检查一次，如果Bot挂了自动重启

BOT_DIR="/root/.openclaw/workspace/psydaily"
BOT_SCRIPT="bot_v2_prebuild.py"
LOG_FILE="$BOT_DIR/bot_v2.log"
PID_FILE="$BOT_DIR/bot.pid"

# 检查Bot是否在运行
check_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            # 检查是否响应Telegram
            if pgrep -f "$BOT_SCRIPT" > /dev/null; then
                echo "$(date): ✅ Bot正在运行 (PID: $PID)"
                return 0
            fi
        fi
    fi
    return 1
}

# 启动Bot
start_bot() {
    echo "$(date): 🚀 启动Bot..."
    cd "$BOT_DIR" || exit 1
    
    # 确保环境变量
    export PATH="$HOME/.local/bin:$PATH"
    
    # 启动Bot
    nohup python3 "$BOT_SCRIPT" >> "$LOG_FILE" 2>&1 &
    NEW_PID=$!
    
    # 保存PID
    echo $NEW_PID > "$PID_FILE"
    
    echo "$(date): ✅ Bot已启动 (PID: $NEW_PID)"
    
    # 发送通知给管理员（可选）
    # curl -s "https://api.telegram.org/bot8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA/sendMessage" \
    #   -d "chat_id=1467459648209813567" \
    #   -d "text=🔄 Bot已自动重启" > /dev/null
}

# 主逻辑
main() {
    if ! check_bot; then
        echo "$(date): ⚠️ Bot未运行，准备重启..."
        
        # 清理可能残留的进程
        pkill -f "$BOT_SCRIPT" 2>/dev/null
        sleep 2
        
        # 启动
        start_bot
    fi
}

# 执行
main
