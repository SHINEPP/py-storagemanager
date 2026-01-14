import base64
import json
import os

'''
v
协议版本号
常见值："2"
基本不影响使用

ps
节点名称（备注）
只用于显示
Clash / v2rayN / Shadowrocket 显示的名字

add
服务器地址
IP 或域名

UUID
VMess 的用户身份标识
核心字段 ❗

aid（alterId）
历史遗留字段
常见值：0
VMess 旧版本用于“多 ID 混淆”
已废弃（Xray / 新客户端直接忽略）
👉 现在必须是 0

net
传输协议类型
决定 VMess 如何“跑在什么上面”
tcp	    纯 TCP
ws	    WebSocket
grpc	gRPC
h2	    HTTP/2
kcp	    mKCP（基本不用）

tls
是否启用 TLS
常见值：
"tls"	    启用 TLS
"" / 不存在	不启用
'''


def generate_vmess(
        ps="Test Node",
        add="1.2.3.4",
        port=443,
        username="",
        net="tcp",
        tls="",
        host="",
        path=""
):
    vmess_dict = {
        "v": "2",
        "ps": ps,
        "add": add,
        "port": str(port),  # ⚠️ 必须是字符串
        "id": username,
        "aid": "0",  # alterId 已废弃，通常为 0
        "net": net,
        "type": "none",
        "host": host,
        "path": path,
        "tls": tls
    }

    json_str = json.dumps(vmess_dict, separators=(",", ":"))
    b64 = base64.b64encode(json_str.encode()).decode()

    return "vmess://" + b64


def generate_config(nodes):
    config = os.path.sep.join(nodes)
    return base64.b64encode(config.encode()).decode()


if __name__ == "__main__":
    configs = []
    configs.append(generate_vmess(
        ps="Mac-V2Ray",
        add="192.168.111.35",
        port=1080,
        username="F9059C91-5B69-4598-A651-045920C5AAC1",
    ))
    print(generate_config(configs))
