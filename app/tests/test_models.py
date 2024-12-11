from django.test import TestCase
from app.models import Transaction


class TransactionModelTest(TestCase):
    def setUp(self):
        self.transaction = Transaction.objects.create(
            name="Salary",
            amount=5000,
            type="Income"
        )

    def test_transaction_creation(self):
        self.assertIsInstance(self.transaction, Transaction)

    def test_transaction_str_method(self):
        self.assertEqual(str(self.transaction), "Salary")
