#!/bin/bash

# 后端部署脚本

echo "===== 开始部署后端服务 ====="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python 3，请先安装Python 3"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 检查是否安装成功
if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    exit 1
fi

# 启动服务
echo "启动后端服务..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 注意：在生产环境中，建议使用进程管理工具（如PM2、systemd）来管理服务
# 示例systemd配置：
# /etc/systemd/system/chira_engine.service
# [Unit]
# Description=Chira Engine Backend Service
# After=network.target
# 
# [Service]
# User=your-username
# WorkingDirectory=/path/to/chira_engine
# ExecStart=/path/to/chira_engine/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
# Restart=always
# 
# [Install]
# WantedBy=multi-user.target