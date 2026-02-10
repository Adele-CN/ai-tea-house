#!/bin/bash
# PsyDaily 自动安装脚本
# 设置所有定时任务

echo "🚀 PsyDaily 自动设置脚本"
echo "=========================="

# 创建必要的目录
mkdir -p /root/.openclaw/workspace/psydaily/logs
mkdir -p /root/.openclaw/workspace/psydaily/data/content

# 给脚本添加执行权限
chmod +x /root/.openclaw/workspace/psydaily/health_check.sh
chmod +x /root/.openclaw/workspace/psydaily/content_generator_v2.py
chmod +x /root/.openclaw/workspace/psydaily/push_scheduler.py

echo "✅ 目录和权限设置完成"

# 安装 cron 任务
echo ""
echo "📅 正在安装定时任务..."

# 先备份现有的 crontab
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || echo "暂无现有crontab"

# 安装新的 crontab
crontab /root/.openclaw/workspace/psydaily/crontab.txt

echo "✅ Cron任务已安装"

# 显示当前任务
echo ""
echo "📋 当前定时任务："
crontab -l

echo ""
echo "=========================="
echo "✅ 设置完成！"
echo ""
echo "功能说明："
echo "  • 每天 04:00 - 生成当天3篇论文内容"
echo "  • 每天 07:00 - 推送晨读论文"
echo "  • 每天 12:00 - 推送午读论文"
echo "  • 每天 18:00 - 推送夜读论文"
echo "  • 每5分钟    - 检查Bot健康状态"
echo ""
echo "日志位置：/root/.openclaw/workspace/psydaily/logs/"
echo ""
echo "现在启动Bot..."

# 启动Bot
cd /root/.openclaw/workspace/psydaily
export PATH="$HOME/.local/bin:$PATH"
nohup python3 bot_v2_prebuild.py > bot_v2.log 2>&1 &
sleep 2

# 检查是否启动成功
if pgrep -f bot_v2_prebuild.py > /dev/null; then
    echo "✅ Bot已启动！"
    echo "PID: $(pgrep -f bot_v2_prebuild.py)"
else
    echo "❌ Bot启动失败，请手动检查"
fi

echo ""
echo "测试命令："
echo "  生成内容：python3 content_generator_v2.py"
echo "  手动推送：python3 push_scheduler.py --slot 1"
echo "  查看日志：tail -f logs/health_check.log"
