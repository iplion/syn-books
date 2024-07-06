# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Rental, Book
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta


@login_required
def home(request):
    rentals = Rental.objects.select_related('book').filter(user=request.user)

    for rental in rentals:
        if rental.return_date is not None and rental.return_date < timezone.now().date():
            rental.now = timezone.now().date()
            rental.is_expired = True
        else:
            rental.now = timezone.now().date()
            rental.is_expired = False

    context = {
        'rentals': rentals,
    }

    return render(request, 'books/home.html', context)


def book_list(request):
    sort_by = request.GET.get('sort_by', 'title')

    books = Book.objects.all().order_by(sort_by)

    context = {
        'books': books,
        'sort_by': sort_by,
    }

    return render(request, 'books/book_list.html', context)


@login_required
def rent_book(request):
    book_id = request.GET.get('book')
    t = request.GET.get('t')
    match t:
        case '1':
            rental_period = relativedelta(weeks=2)
        case '2':
            rental_period = relativedelta(months=1)
        case '3':
            rental_period = relativedelta(months=3)
        case _:
            rental_period = 0

    if book_id and t:
        book = get_object_or_404(Book, id=book_id)

        book.status = 'rented'
        rental = Rental(
            user=request.user,
            book=book,
            return_date=datetime.now().date() + rental_period,
        )

        book.save()
        rental.save()

        return redirect('book_list')
        # return redirect('home')

    return redirect('book_list')


@login_required
def buy_book(request):
    book_id = request.GET.get('book')

    if book_id:
        book = get_object_or_404(Book, id=book_id)

        book.status = 'bought'
        rental = Rental(
            user=request.user,
            book=book,
            return_date=None,
        )

        book.save()
        rental.save()

        return redirect('book_list')
        # return redirect('home')

    return redirect('book_list')
