from django.contrib import admin
from cms.models import Book, Impression

# 管理サイトにモデルを登録
# Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'page')  # 一覧に表示する項目
    list_display_links = ('id', 'name')                 # 修正リンクでクリックできる項目
admin.site.register(Book, BookAdmin)


# Impression
class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')        # 一覧に表示する項目
    list_display_links = ('id', 'comment')  # 修正リンクでクリックできる項目
admin.site.register(Impression, ImpressionAdmin)
