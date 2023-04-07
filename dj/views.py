import json
from django.http import HttpResponse
from django.shortcuts import render
from . import until


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        param = json.loads(request.body.decode('utf-8'))
        username = param['username']
        password = param['password']
        sql = 'select * from `tb_user` where user_name = "{0}" and password = "{1}" limit 0,1'.format(username,
                                                                                                      password)
        res = until.qurey(sql)
        if res == ():
            data = '该用户未注册，请注册后在登录'
            return HttpResponse(data)
        else:
            data = "登录成功"
            return HttpResponse(data)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        param = json.loads(request.body.decode('utf-8'))
        username = param['username']
        password = param['password']
        sql = 'select * from tb_user where user_name = "{0}" and password = "{1}" limit 0,1'.format(username, password)
        res = until.qurey(sql)
        if res != ():
            data = '该用户已经注册'
            return HttpResponse(data)
        else:
            sql = 'insert into tb_user(`user_name`,`password`) values ("%s","%s")' % (username, password)
            until.insert(sql)
            data = "注册成功"
            return HttpResponse(data)


def all_movie(request):
    sql = 'select * from movie'
    res = until.qurey(sql)
    data = []
    for i in res:
        a = {
            'id': i[0],
            'name': i[2],
            'img': i[6]
        }
        data.append(a)
    data = {
        'data': data
    }
    return render(request, 'allmovie.html', data)


def movie_data(request):
    id = request.GET['id']
    sql = 'select * from movie where id = {0}'.format(repr(id))
    res = until.qurey(sql)
    for i in res:
        data0 = {
            'id': i[0],
            'name': i[2],
            'detail': i[3],
            'rank': i[4],
            'score': i[5],
            'img': i[6]
        }
    sql = 'select * from comment where movieid = {0}'.format(repr(id))
    res = until.qurey(sql)
    data1 = []
    text = []
    for i in res:
        a = {
            'text': i[1],
            'NLP': i[2],
            'score': i[3],
        }
        data1.append(a)
        text.append(i[1])
    until.wordcloud(text)
    data = {'data1': data1, 'data0': data0}
    return render(request, 'moviedata.html', data)


def getnlp(request):
    id = request.GET['id']
    sql = 'select * from comment where movieid = {0}'.format(repr(id))
    res = until.qurey(sql)
    data1 = []
    for i in res:
        data1.append(list(i)[2])
    return HttpResponse(json.dumps(data1))


def getLDA(request):
    id = request.GET['id']
    sql = 'select * from comment where movieid = {0}'.format(repr(id))
    res = until.qurey(sql)
    data1 = []
    for i in res:
        data1.append(i[1])
    a = until.LDA(data1)
    b, c = [], []
    for i in a:
        b.append(i[0])
        c.append(i[1])
    a = [b, c]
    return HttpResponse(json.dumps(a))


def getscore(request):
    id = request.GET['id']
    sql = 'select * from comment where movieid = {0}'.format(repr(id))
    res = until.qurey(sql)
    data = []
    num = []
    for i in res:
        if list(i)[3] not in data:
            data.append(list(i)[3])
    for i in data:
        a = 0
        for j in res:
            if j[3] == i:
                a += 1
        num.append(a)
    jso = []
    for i in range(len(data)):
        a = {
            'value': num[i],
            'name': data[i]
        }
        jso.append(a)
    return HttpResponse(json.dumps(jso))


def visualization(request):
    if request.method == 'GET':
        return render(request, 'visualization.html')
    else:
        alldata = []
        sql = 'select * from movie'
        res = until.qurey(sql)
        score = []
        for i in res:
            score.append(i[5])
        x = ['小于8.5分', '8.5-9.0分', '9.0-9.5分', '大于9.5分']
        y = [0, 0, 0, 0]
        for i in score:
            if float(i) < 8.5:
                y[0] += 1
            elif 8.5 <= float(i) < 9.0:
                y[1] += 1
            elif 9.0 <= float(i) < 9.5:
                y[2] += 1
            else:
                y[3] += 1
        data = []
        for i in range(len(x)):
            a = {
                'value': y[i],
                'name': x[i]
            }
            data.append(a)
        alldata.append(data)

        sql = 'select * from comment'
        res = until.qurey(sql)
        data = []
        for i in res:
            data.append(float(i[2]))
        x = ['小于0.4分', '0.4-0.6分', '0.6-0.8分', '0.8-0.9分', '大于0.9分']
        y = [0, 0, 0, 0, 0]
        for i in data:
            if float(i) < 0.4:
                y[0] += 1
            elif 0.4 <= float(i) < 0.6:
                y[1] += 1
            elif 0.6 <= float(i) < 0.8:
                y[2] += 1
            elif 0.8 <= float(i) < 0.9:
                y[3] += 1
            else:
                y[4] += 1
        data = []
        for i in range(len(x)):
            a = {
                'value': y[i],
                'name': x[i]
            }
            data.append(a)
        alldata.append(data)

        sql = 'select * from comment'
        res = until.qurey(sql)
        data = []
        num = []
        for i in res:
            if list(i)[3] not in data:
                data.append(list(i)[3])
        for i in data:
            a = 0
            for j in res:
                if j[3] == i:
                    a += 1
            num.append(a)
        a = [data, num]
        alldata.append(a)
        return HttpResponse(json.dumps(alldata))
