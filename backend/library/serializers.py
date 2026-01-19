from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import Book, Member, IssueRecord
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'publication_date', 'total_copies',
                  'available_copies', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'member_id', 'phone', 'address', 'date_joined', 'is_active']
        read_only_fields = ['date_joined']


class IssueRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    member = MemberSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source='member', write_only=True)

    class Meta:
        model = IssueRecord
        fields = ['id', 'book', 'book_id', 'member', 'member_id', 'issue_date', 'due_date',
                  'return_date', 'status', 'fine_amount', 'created_at', 'updated_at']
        read_only_fields = ['issue_date', 'return_date', 'status', 'fine_amount', 'created_at', 'updated_at']


class IssueBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()
    due_date = serializers.DateField(required=False)

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
            if book.available_copies <= 0:
                raise serializers.ValidationError("No copies available for this book.")
            return value
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

    def validate_member_id(self, value):
        try:
            member = Member.objects.get(id=value, is_active=True)
            return value
        except Member.DoesNotExist:
            raise serializers.ValidationError("Member not found or inactive.")

    def create(self, validated_data):
        book = Book.objects.get(id=validated_data['book_id'])
        member = Member.objects.get(id=validated_data['member_id'])
        
        # Check if member already has this book issued
        existing_issue = IssueRecord.objects.filter(
            book=book, member=member, status='issued'
        ).first()
        
        if existing_issue:
            raise serializers.ValidationError("Member already has this book issued.")

        # Calculate due date (default: 14 days from now)
        due_date = validated_data.get('due_date')
        if not due_date:
            due_date = timezone.now().date() + timedelta(days=14)

        issue_record = IssueRecord.objects.create(
            book=book,
            member=member,
            due_date=due_date
        )

        # Update book available copies
        book.available_copies -= 1
        book.save()

        return issue_record


class ReturnBookSerializer(serializers.Serializer):
    issue_record_id = serializers.IntegerField()

    def validate_issue_record_id(self, value):
        try:
            issue_record = IssueRecord.objects.get(id=value, status__in=['issued', 'overdue'])
            return value
        except IssueRecord.DoesNotExist:
            raise serializers.ValidationError("Issue record not found or already returned.")

    def create(self, validated_data):
        issue_record = IssueRecord.objects.get(id=validated_data['issue_record_id'])
        
        # Calculate fine if overdue
        issue_record.calculate_fine()
        
        # Update issue record
        from django.utils import timezone
        issue_record.return_date = timezone.now().date()
        issue_record.status = 'returned'
        issue_record.save()

        # Update book available copies
        book = issue_record.book
        book.available_copies += 1
        book.save()

        return issue_record
