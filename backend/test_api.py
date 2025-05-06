import requests
import json

def test_register_api():
    url = "http://localhost:8000/api/auth/register/"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 测试数据
    data = {
        "username": "testuser123",
        "password": "testpassword123",
        "userType": "freelancer"
    }
    
    # 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # 打印详细信息
    print(f"状态码: {response.status_code}")
    print(f"响应头: {response.headers}")
    
    try:
        print(f"响应内容: {response.json()}")
    except:
        print(f"响应内容不是JSON格式: {response.text}")

if __name__ == "__main__":
    test_register_api() 