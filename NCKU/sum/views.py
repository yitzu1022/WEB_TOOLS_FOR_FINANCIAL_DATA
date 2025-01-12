from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def sum(request):
    return render(request, 'sum.html') # 這裡是將 sum.html 這個模板回傳給使用者
def ajax_sum(request):
    a = int(request.GET['num1'])
    b = int(request.GET['num2'])
    response = {'sum': a+b}
    return JsonResponse(response) # 這裡是將 response 這個字典回傳給使用者