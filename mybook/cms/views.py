from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView

from cms.models import Book, Impression
from cms.forms import BookForm, ImpressionForm


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
        if form.is_valid():     # フォームのバリデーション
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


def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:
        # impression_id が指定されているとき、修正する Impression オブジェクトを取得
        impression = get_object_or_404(Impression, pk=impression_id)
    else:
        # impression_id が指定されていないとき、新しく追加する Impression オブジェクトを作成
        impression = Impression()

    if request.method == 'POST':
        # POST されたデータからフォームを作成
        form = ImpressionForm(request.POST, instance=impression)
        if form.is_valid():     # フォームのバリデーション
            # Impression オブジェクトを保存
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            impression.save()
            # 感想一覧のページにリダイレクト
            return redirect('cms:impression_list', book_id=book_id)
    else:
        # GET のとき、Impression インスタンスからフォームを作成
        form = ImpressionForm(instance=impression)

    # 編集ページを出力
    return render(request,
                  'cms/impression_edit.html',                                       # ビューのテンプレート
                  dict(form=form, book_id=book_id, impression_id=impression_id))    # テンプレートに渡すデータ


def impression_delete(request, book_id, impression_id):
    """感想の削除"""
    # 指定された感想を削除
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    # 感想の一覧のページにリダイレクト
    return redirect('cms:impression_list', book_id=book_id)


class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name = 'impressions'
    template_name = 'cms/impression_list.html'
    paginate_by = 2     # ページングの単位

    def get(self, request, *args, **kwargs):
        # 親の Book オブジェクトとそれに関連付いた Impression オブジェクトを取得する
        book = get_object_or_404(Book, pk=kwargs['book_id'])
        impressions = book.impressions.all().order_by('id')
        # ListView のアイテムリストに設定
        self.object_list = impressions

        # ListView をレンダリングして出力
        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)
