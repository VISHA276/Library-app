from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Book, Member, IssueRecord
from .serializers import (
    UserSerializer, RegisterSerializer, BookSerializer, MemberSerializer,
    IssueRecordSerializer, IssueBookSerializer, ReturnBookSerializer
)
from django.db.models import Q


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow anyone to view books

    def get_queryset(self):
        queryset = Book.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(isbn__icontains=search)
            )
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available books (available_copies > 0)"""
        books = self.get_queryset().filter(available_copies__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Member.objects.filter(is_active=True)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(member_id__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['get'])
    def issues(self, request, pk=None):
        """Get all issue records for a member"""
        member = self.get_object()
        issues = IssueRecord.objects.filter(member=member).order_by('-issue_date')
        serializer = IssueRecordSerializer(issues, many=True)
        return Response(serializer.data)


class IssueRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IssueRecord.objects.all()
    serializer_class = IssueRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = IssueRecord.objects.all()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    @action(detail=False, methods=['post'])
    def issue(self, request):
        """Issue a book to a member"""
        serializer = IssueBookSerializer(data=request.data)
        if serializer.is_valid():
            issue_record = serializer.save()
            response_serializer = IssueRecordSerializer(issue_record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        """Return a book"""
        serializer = ReturnBookSerializer(data=request.data)
        if serializer.is_valid():
            issue_record = serializer.save()
            response_serializer = IssueRecordSerializer(issue_record)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user and create a member"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create member profile
            import random
            member_id = f"M{random.randint(10000, 99999)}"
            while Member.objects.filter(member_id=member_id).exists():
                member_id = f"M{random.randint(10000, 99999)}"
            
            member = Member.objects.create(
                user=user,
                member_id=member_id
            )
            
            return Response({
                'user': UserSerializer(user).data,
                'member': MemberSerializer(member).data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user information"""
        user_serializer = UserSerializer(request.user)
        try:
            member = request.user.member
            member_serializer = MemberSerializer(member)
            return Response({
                'user': user_serializer.data,
                'member': member_serializer.data
            })
        except Member.DoesNotExist:
            return Response({
                'user': user_serializer.data,
                'member': None
            })
