#encoding:UTF-8

from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from htable import *
import json
import os
import sys
import urllib


reload(sys)
sys.setdefaultencoding('utf8')

# Create your views here.
def index(request):
    return render_to_response('index.html')

def ajax_getData(request):
    con_str = request.POST["conn"]
    tbl = request.POST["tbl"]
    print request.POST

    rk_lst = []
    for rk in request.POST["rk"].split(','):
        if rk.strip() != "":
            rk_lst.append(rk.strip())
    columns = []
    for col in request.POST["cols"].split(','):
        if col != "":
            col_n = col.strip().strip("\"'").encode('utf-8')
            columns.append(col_n)
    data = Htable(con_str).getData(tbl, rk_lst, columns)
#     data1 = json.dumps(data)
    return JsonResponse(data, safe=False)

def ajax_put(request):
    print request.POST
    con_str = request.POST["conn"]
    tbl = request.POST["tbl"]
    rk_lst = []
    for rk in request.POST["rk"].split(','):
        if rk != "":
            rk_lst.append(rk)
            
    in_str = request.POST["input"]
#     try:
#         inputs = json.loads(in_str)
#     except Exception:
#         return JsonResponse({"status":"fail","msg":"Incorrect Json Format."})
    try:
        inputs = eval(in_str)
    except Exception as e:
        return JsonResponse({"status":"fail","msg":"Incorrect Json Format."})
#     inputs = json.loads(in_str, encoding="utf-8")
#     print inputs
    if len(rk_lst) != len(inputs):
        return JsonResponse({"status":"fail","msg":"list mismatch."})
    totalCnt = len(rk_lst)
    seccCnt = 0
    fail_lst = []
    for i in range(0, totalCnt):
        rk = rk_lst[i].strip()
        rs = Htable(con_str).putData(tbl, rk, inputs[i])
        if rs == "secc":
            seccCnt += 1
        else:
            fail_lst.append(str(i))
    if totalCnt != seccCnt:
        print "".join(fail_lst)
        stat = "fail"
        msg = "totalCnt: %d, seccCnt: %d, fail_lst: %s" % (totalCnt, seccCnt, "".join(fail_lst))
    else:
        stat = "secc"
        msg = ""
    return JsonResponse({"status":stat ,"msg":msg})

def ajax_del(request):
    con_str = request.POST["conn"]
    tbl = request.POST["tbl"]
    rk_lst = []
    for rk in request.POST["rk"].split(','):
        if rk != "":
            rk_lst.append(rk)
    
    columns = []
    for col in request.POST["cols"].split(','):
        if col != "":
            columns.append(col.strip().strip("\"'").encode('utf-8'))
    totalCnt = len(rk_lst)
    seccCnt = 0
    fail_lst = []
    for i in range(0, totalCnt):
        rk = rk_lst[i].strip()
        rs = Htable(con_str).delData(tbl, rk, columns)
        if rs == "secc":
            seccCnt += 1
        else:
            fail_lst.append(str(i))
    if totalCnt != seccCnt:
        msg = "totalCnt: %d, seccCnt: %d, fail_lst: %s" % (totalCnt, seccCnt, "".join(fail_lst))
    else:
        msg = ""
    return JsonResponse({"status":"secc","msg":msg})
