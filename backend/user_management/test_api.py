import requests
import json

"""
用户资料更新API测试脚本

使用方法：
1. 确保Django服务器已启动
2. 运行此脚本测试API功能
"""

# 服务器基础URL
BASE_URL = 'http://localhost:8000/api/auth/'

# 测试用户凭据
TEST_USERNAME = 'admin'
TEST_PASSWORD = 'admin123'


def test_user_profile_update():
    """测试用户资料更新API"""
    # 1. 登录获取令牌（实际项目中应该有登录API）
    # 这里使用模拟令牌，实际项目中应该调用登录API获取
    token = 'mock-jwt-token-for-admin'
    
    # 2. 准备要更新的用户资料
    profile_data = {
        'email': 'updated_admin@example.com',
        'first_name': '管理员',
        'last_name': '测试',
        'phone': '13800138001',
        'bio': '这是一个测试更新的个人简介',
        'skills': 'Python, Django, REST API'
    }
    
    # 3. 发送更新请求
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.put(
            f'{BASE_URL}profile/', 
            data=json.dumps(profile_data),
            headers=headers
        )
        
        # 4. 检查响应
        if response.status_code == 200:
            print('用户资料更新成功!')
            print('更新后的用户资料:')
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f'更新失败! 状态码: {response.status_code}')
            print('错误信息:', response.text)
    
    except Exception as e:
        print(f'请求异常: {str(e)}')
        print('请确保Django服务器已启动，并且API路由配置正确')


if __name__ == '__main__':
    print('开始测试用户资料更新API...')
    test_user_profile_update()