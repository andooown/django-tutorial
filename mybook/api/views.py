import json
from collections import OrderedDict
from django.http import HttpResponse
from cms.models import Book


def render_json_response(request, data, status=None):
    """response を JSON で返却"""
    # データを JSON 文字列に変換
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    # コールバックを取得
    callback = request.GET.get('callback')
    if not callback:
        # POSTで JSONP の場合
        callback = request.POST.get('callback')

    # レスポンスを生成
    if callback:
        # JSONP の場合
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
    else:
        response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    # レスポンスを返す
    return response


def book_list(request):
    """書籍と感想のJSONを返す"""
    books = []  # 書籍の一覧
    for book in Book.objects.all().order_by('id'):
        impressions = []    # 現在の書籍に紐付いた感想の一覧
        for impression in book.impressions.order_by('id'):
            # 感想を追加
            impression_dict = OrderedDict([
                ('id', impression.id),
                ('comment', impression.comment),
            ])
            impressions.append(impression_dict)
        # 書籍を追加
        book_dict = OrderedDict([
            ('id', book.id),
            ('name', book.name),
            ('publisher', book.publisher),
            ('page', book.page),
            ('impressions', impressions)
        ])
        books.append(book_dict)
    # レスポンスを JSON で生成する
    data = OrderedDict([ ('books', books) ])
    return render_json_response(request, data)