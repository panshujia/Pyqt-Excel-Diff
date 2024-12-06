chcp 65001
@echo off
if exist venv\Scripts\activate (
    echo 安装依赖...
    pip install -r requirements.txt
) else (
    echo 创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate
    echo 安装依赖...
    pip install -r requirements.txt
)

call venv\Scripts\activate
echo Diff 启动！！！！
python main.py