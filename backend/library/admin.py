from django.contrib import admin
from .models import Book, Member, IssueRecord


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'total_copies', 'available_copies', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'author', 'isbn']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'member_id', 'phone', 'date_joined', 'is_active']
    list_filter = ['is_active', 'date_joined']
    search_fields = ['user__username', 'user__email', 'member_id']


@admin.register(IssueRecord)
class IssueRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'issue_date', 'due_date', 'return_date', 'status', 'fine_amount']
    list_filter = ['status', 'issue_date', 'due_date']
    search_fields = ['book__title', 'member__user__username', 'member__member_id']
