from django.shortcuts import render
from django.http import JsonResponse
# import talib

# Create your views here.
def HW1(request):
    return render(request, 'HW1.html') 

def ajax_showStock(request):
    a = int(request.GET['d'])
    response = {'sum': a} #隨便先寫的
    # print("TA-Lib version:", talib.__version__)

    return JsonResponse(response) # 這裡是將 response 這個字典回傳給使用者

