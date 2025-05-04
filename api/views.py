from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt  # 添加CSRF豁免装饰器
def check_number(request):
    """
    检查数字是奇数还是偶数的API视图
    偶数返回1，奇数返回0
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number = int(data.get('number', 0))
            
            # 判断是否为偶数
            if number % 2 == 0:
                result = 1  # 偶数
            else:
                result = 0  # 奇数
                
            return JsonResponse({
                'number': number,
                'result': result,
                'is_even': result == 1
            })
        except (ValueError, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
