from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from cms.models import Book
from cms.forms import BookForm


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
    if book_id:
        # book_id が指定されているとき、修正する Book オブジェクトを取得
        book = get_object_or_404(Book, pk=book_id)
    else:
        # book_id が指定されていないとき、新しく追加する Book オブジェクトを作成
        book = Book()

    if request.method == 'POST':
        # POST されたデータからフォームを作成
        form = BookForm(request.POST, instance=book)
        if form.is_valid():  # フォームのバリデーション
            # Book オブジェクトを保存
            book = form.save(commit=False)
            book.save()
            # 書籍一覧のページにリダイレクト
            return redirect('cms:book_list')
    else:
        # GET のとき、Book インスタンスからフォームを作成
        form = BookForm(instance=book)

    # 編集ページを出力
    return render(request, 'cms/book_edit.html', dict(form=form, book_id=book_id))


def book_delete(request, book_id):
    """書籍の削除"""
    # 指定された Book オブジェクトを取得し、削除する
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    # 書籍一覧のページにリダイレクト
    return redirect('cms:book_list')
