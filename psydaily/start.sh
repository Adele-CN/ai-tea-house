#!/bin/bash
# PsyDaily 启动脚本

echo "🚀 启动 PsyDaily..."

cd /root/.openclaw/workspace/psydaily

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python 3"
    exit 1
fi

# 安装依赖（如果需要）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "📦 安装依赖..."
source venv/bin/activate
pip install -q -r requirements.txt

# 运行程序
echo "🎯 运行演示..."
python3 src/main.py
