#encoding=utf-8
"""
Definition of views.
"""

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from app.forms import ProfileForm # 上传图片的图表
from app.models import Profile # 保存上传图片相关信息的模型
import urllib2
import json
import PIL
import httplib, urllib, base64

def index(request):

    return render(request, 'app/index.html')



def search(request):
    url = 'https://ussouthcentral.services.azureml.net/workspaces/affa727963bf4974bf07b6db68f32bb1/services/dfb57bed440548eab48c1cd53c18fc55/execute?api-version=2.0'
    api_key = '+s2pdt/AuMoWc2vM4b83GE3tkcdUK98ZCpZlcANMecX7YmV9XVnz9EtYZa6eKRsrkTS6HyAx6PjGRSX4Y4CFAA=='  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    data = {
        "Inputs": {
            "input1": {
                "ColumnNames": [
                    "symboling",
                    "normalized-losses",
                    "make",
                    "fuel-type",
                    "aspiration",
                    "num-of-doors",
                    "body-style",
                    "drive-wheels",
                    "engine-location",
                    "wheel-base",
                    "length",
                    "width",
                    "height",
                    "curb-weight",
                    "engine-type",
                    "num-of-cylinders",
                    "engine-size",
                    "fuel-system",
                    "bore",
                    "stroke",
                    "compression-ratio",
                    "horsepower",
                    "peak-rpm",
                    "city-mpg",
                    "highway-mpg",
                    "price"
                ],
                "Values": [
                    [
                        request.GET.get("symboling","2"),
                        request.GET.get("normalized-losses","164"),
                        request.GET.get("make","audi"),
                        request.GET.get("fuel-type","gas"),
                        request.GET.get("aspiration","std"),
                        request.GET.get("num-of-doors","four"),
                        request.GET.get("body-style","sedan"),
                        request.GET.get("drive-wheels","fwd"),
                        request.GET.get("engine-location","front"),
                        request.GET.get("wheel-base","99.8"),
                        request.GET.get("length","176.6"),
                        request.GET.get("width","66.2"),
                        request.GET.get("height","54.3"),
                        request.GET.get("curb-weight","2337"),
                        request.GET.get("engine-type","ohc"),
                        request.GET.get("num-of-cylinders","four"),
                        request.GET.get("engine-size","109"),
                        request.GET.get("fuel-system","mpfi"),
                        request.GET.get("bore","3.19"),
                        request.GET.get("stroke","3.4"),
                        request.GET.get("compression-ratio","10"),
                        request.GET.get("horsepower","102"),
                        request.GET.get("peak-rpm","5500"),
                        request.GET.get("city-mpg","24"),
                        request.GET.get("highway-mpg","30"),
                        request.GET.get("price","0"),
                    ],

                ]
            }
        },
        "GlobalParameters": {}
    }
    body = str.encode(json.dumps(data))
    print body
    req = urllib2.Request(url, body, headers)
    dict = {'error':'1'}
    try:
        response = urllib2.urlopen(req)
        result = response.read()
        price = json.loads(result)
        price = price["Results"]
        price = price["output1"]
        price = price["value"]
        price = price["Values"]
        price = price[0]
        price = price[-1]
        print price
        dict = {'price': price}

    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read()))
    return JsonResponse(dict)

def face_recog(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '006437565f784716a0f722789b2e4215',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })
    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        rurl = 'http://mydns.koreasouth.cloudapp.azure.com' + url
        print rurl
        body = {'url': rurl}
        conn.request("POST", "/face1.0/detect?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



def uploadImg(request):
    return render(request, 'app/uploadimg.html')

def save_profile(request):
    print request.method
    if request.method == "POST":
        # 接收 post 方法传回后端的数据
        MyProfileForm = ProfileForm(request.POST, request.FILES)
        # 检验表单是否通过校验
        print MyProfileForm.is_valid()
        if MyProfileForm.is_valid():
            # 构造一个 Profile 实例
            profile = Profile()
            # 获取name
            profile.name = MyProfileForm.cleaned_data["name"]
            # 获取图片
            profile.picture = MyProfileForm.cleaned_data["picture"]
            # 保存
            profile.save()
            print profile.name,profile.picture.url
            face_recog(profile.picture.url)
            return redirect(to='index')
    return redirect(to='login')


