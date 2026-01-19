"""
Management command to load sample data for demonstration
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Book, Member, IssueRecord
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Load sample data (books, members, issue records) for demonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))

        # Create sample books
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'publication_date': date(1925, 4, 10),
                'total_copies': 5,
                'available_copies': 3,
                'description': 'A classic American novel about the Jazz Age and the American Dream.'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'publication_date': date(1960, 7, 11),
                'total_copies': 4,
                'available_copies': 2,
                'description': 'A gripping tale of racial injustice and childhood innocence in the American South.'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'publication_date': date(1949, 6, 8),
                'total_copies': 6,
                'available_copies': 4,
                'description': 'A dystopian social science fiction novel about totalitarian control.'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'publication_date': date(1813, 1, 28),
                'total_copies': 5,
                'available_copies': 5,
                'description': 'A romantic novel of manners that critiques the British landed gentry.'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'isbn': '9780316769174',
                'publication_date': date(1951, 7, 16),
                'total_copies': 3,
                'available_copies': 1,
                'description': 'A controversial novel about teenage rebellion and alienation.'
            },
            {
                'title': 'Lord of the Flies',
                'author': 'William Golding',
                'isbn': '9780571056866',
                'publication_date': date(1954, 9, 17),
                'total_copies': 4,
                'available_copies': 3,
                'description': 'A story about a group of British boys stranded on an uninhabited island.'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780547928227',
                'publication_date': date(1937, 9, 21),
                'total_copies': 5,
                'available_copies': 4,
                'description': 'A fantasy novel about Bilbo Baggins and his unexpected journey.'
            },
            {
                'title': 'Fahrenheit 451',
                'author': 'Ray Bradbury',
                'isbn': '9781451673319',
                'publication_date': date(1953, 10, 19),
                'total_copies': 3,
                'available_copies': 2,
                'description': 'A dystopian novel about censorship and the power of books.'
            },
            {
                'title': 'Animal Farm',
                'author': 'George Orwell',
                'isbn': '9780452284241',
                'publication_date': date(1945, 8, 17),
                'total_copies': 4,
                'available_copies': 3,
                'description': 'An allegorical novella about farm animals rebelling against their human farmer.'
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'isbn': '9780061122415',
                'publication_date': date(1988, 1, 1),
                'total_copies': 5,
                'available_copies': 4,
                'description': 'A philosophical novel about following your dreams and listening to your heart.'
            },
        ]

        books = []
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            books.append(book)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))

        # Create sample members (if they don't exist)
        members_data = [
            {
                'username': 'john_doe',
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'member_id': 'M12345',
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'member_id': 'M12346',
            },
            {
                'username': 'bob_wilson',
                'email': 'bob.wilson@example.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'member_id': 'M12347',
            },
        ]

        members = []
        for member_data in members_data:
            user, created = User.objects.get_or_create(
                username=member_data['username'],
                defaults={
                    'email': member_data['email'],
                    'first_name': member_data['first_name'],
                    'last_name': member_data['last_name'],
                }
            )
            if created:
                user.set_password('demo123')  # Set a default password
                user.save()

            member, created = Member.objects.get_or_create(
                user=user,
                defaults={'member_id': member_data['member_id']}
            )
            members.append(member)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created member: {member.user.get_full_name()}'))

        # Create some issue records
        issue_records_created = 0
        for i in range(5):
            book = random.choice(books)
            member = random.choice(members)
            
            # Only issue if book is available
            if book.available_copies > 0:
                # Check if already issued to this member
                existing = IssueRecord.objects.filter(
                    book=book,
                    member=member,
                    status__in=['issued', 'overdue']
                ).exists()
                
                if not existing:
                    issue_date = date.today() - timedelta(days=random.randint(1, 10))
                    due_date = issue_date + timedelta(days=14)
                    
                    issue_record = IssueRecord.objects.create(
                        book=book,
                        member=member,
                        issue_date=issue_date,
                        due_date=due_date,
                        status='issued'
                    )
                    
                    # Update book available copies
                    book.available_copies -= 1
                    book.save()
                    
                    issue_records_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created issue record: {book.title} -> {member.user.get_full_name()}'
                        )
                    )

        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(books)} books'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(members)} members'))
        self.stdout.write(self.style.SUCCESS(f'   - {issue_records_created} active issue records'))
        self.stdout.write(self.style.WARNING('\nDemo Member Credentials:'))
        self.stdout.write(self.style.WARNING('   Username: john_doe, Password: demo123'))
        self.stdout.write(self.style.WARNING('   Username: jane_smith, Password: demo123'))
        self.stdout.write(self.style.WARNING('   Username: bob_wilson, Password: demo123'))
