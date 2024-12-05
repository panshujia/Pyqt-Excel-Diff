if [ -d "venv" ]; then
    echo "安装依赖..."
    pip install -r requirements.txt
else
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "安装依赖..."
    pip install -r requirements.txt
fi

source venv/bin/activate
echo "Diff 启动！！！！"
python3 main.py