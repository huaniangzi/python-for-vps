import paramiko

# 定义服务器列表，包括服务器名称、IP地址、端口号、用户名和密码
servers = [

    {"name": "美国", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "不丹", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "毛里求斯", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   

    # 添加更多服务器
]


# 定义更新操作
def update_server(name, hostname, port, username, password):
    try:

       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)


        # 执行步骤1: 更新操作
        print(f" {name} 更新")
        stdin, stdout, stderr = client.exec_command("apt update -y && apt install -y curl wget sudo socat htop")
        
        print(f"正在更新:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"更新成功")
        else:
            print(f"更新失败")
        
        print()


        print(f"{name} 安装 Docker")
        stdin, stdout, stderr = client.exec_command("wget -qO- https://get.docker.com/ | sh")

        print(f"正在安装 Docker:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装 Docker 成功")
        else:
            print(f"安装 Docker 失败")

        print()


        print(f"在服务器 {name} 上安装流量出售工具")
        stdin, stdout, stderr = client.exec_command("docker run -d --name tmd --restart=always traffmonetizer/cli start accept --token VM+OdtNp5mupfl8I2w0EZswkOJ8WSuTuMe/kDV02gS8=")

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装成功")
        else:
            print(f"安装失败")


        stdin, stdout, stderr = client.exec_command("docker ps -a")

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")
                print("")

        # 关闭 SSH 连接
        client.close()



    except Exception as e:
        print(f"连接服务器 {name} ({hostname}:{port}) 失败: {e}")


# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    update_server(name, hostname, port, username, password)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")
