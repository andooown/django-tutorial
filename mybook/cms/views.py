from django.shortcuts import render
from django.http import HttpResponse

from cms.models import Book


def book_list(request):
    """書籍の一覧"""
    # 書籍の一覧を取得
    books = Book.objects.all().order_by('id')
    # ビューを出力
    return render(request,
                  'cms/book_list.html',     # ビューのテンプレート
                  {'books': books})         # テンプレートに渡すデータ


def book_edit(request, book_id=None):
    """書籍の編集"""
    return HttpResponse('書籍の編集')


def book_delete(request, book_id):
    """書籍の削除"""
    return HttpResponse('書籍の削除')
