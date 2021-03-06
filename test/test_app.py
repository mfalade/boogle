"""Test Application Instance Properties."""
import unittest
from flask import Flask


from boogle import create_app
from boogle.books.models import Books


class AppTest(unittest.TestCase):
    def setUp(self):
        """Basic App setup.

        Create instance of client to handle requests.
        """
        self.app = create_app('test')
        self.client = self.app.test_client()


    def test_main_route_works_as_expected(self):
        """Test that index route works as expected."""
        vr = self.client.get('/')
        self.assertEqual(vr.status_code, 200)


class BooksModelTest(unittest.TestCase):
    def setUp(self):
        self.Books = Books
        self.Books.ALL_BOOKS = {'books': [{'category': 'action', 'name': 'test book one'}]}


    def test_search_returns_empty_list_when_string_not_in_category_name(self):
        result = self.Books.search_by('test', filters='category')
        self.assertEqual([], result)


    def test_search_returns_empty_list_with_string_not_in_book_name(self):
        search_term = 'ThisBookShouldNotExist'
        result = self.Books.search_by(search_term, filters='name')
        self.assertEqual([], result)

    def test_search_returns_empty_list_when_string_not_in_book_name_or_category_name(self):
        search_term = 'ThisStringShouldNotExist'
        result = self.Books.search_by(search_term)
        self.assertEqual([], result)

    def test_search_returns_non_empty_list_with_string_that_exists_in_book_name(self):
        search_term = 'test'
        result = self.Books.search_by(search_term, filters='name')
        self.assertEqual(1, len(result))

    def test_search_returns_non_empty_list_with_string_that_exists_in_category_name(self):
        search_term = 'action'
        result = self.Books.search_by(search_term, filters='category')
        self.assertEqual(1, len(result))

    def test_search_returns_non_empty_list_with_keyword_that_exists_in_both_book_and_category_name(self):
        search_term = 'action'
        result = self.Books.search_by(search_term, filters='keyword')
        self.assertEqual(1, len(result))
