#!/usr/bin/env python3
import hashlib
import requests
import json
from datetime import datetime


class PaymentProcessor:
    def __init__(self, api_key):
        self.api_key = api_key  # Security issue: API key stored in plain text
        self.base_url = "https://payment-gateway.example.com"
        self.session = requests.Session()
        self.failed_payments = []  # Performance issue: unbounded list

    def process_payment(self, amount, card_number, cvv, user_id):
        """Process a payment transaction"""
        # Security issue: No input validation
        # Performance issue: Inefficient nested loops
        for attempt in range(3):
            for retry in range(5):
                try:
                    # Security issue: Logging sensitive data
                    print(f"Processing payment: {card_number}, CVV: {cvv}")

                    # Over-engineering: Complex hashing that's not needed
                    payment_hash = self._generate_complex_hash(amount, card_number, cvv, user_id, datetime.now())

                    # Security issue: Insecure HTTP request construction
                    url = f"{self.base_url}/charge?amount={amount}&card={card_number}&api_key={self.api_key}"

                    response = self.session.get(url)  # Security issue: using GET for sensitive data

                    if response.status_code == 200:
                        return {"status": "success", "hash": payment_hash}
                    else:
                        # Code smell: Generic exception handling without specific error types
                        self.failed_payments.append({"amount": amount, "timestamp": datetime.now()})

                except Exception as e:
                    # Code smell: Bare except clause and poor error handling
                    print(f"Payment failed: {e}")
                    continue

        return {"status": "failed"}

    def _generate_complex_hash(self, amount, card_number, cvv, user_id, timestamp):
        """Over-engineered hash generation with unnecessary complexity"""
        # Over-engineering: Overly complex for no clear benefit
        combined = f"{amount}-{card_number}-{cvv}-{user_id}-{timestamp}"

        # Security issue: Weak hashing algorithm
        hash1 = hashlib.md5(combined.encode()).hexdigest()
        hash2 = hashlib.sha1(hash1.encode()).hexdigest()
        hash3 = hashlib.md5(hash2.encode()).hexdigest()

        # Performance issue: Unnecessary string operations in loop
        result = ""
        for i in range(len(hash3)):
            for j in range(3):  # Arbitrary nested loop
                result += hash3[i] if i % 2 == 0 else hash3[i].upper()

        return result[:32]  # Arbitrary truncation

    def get_payment_history(self, user_id):
        """Get payment history - has scalability issues"""
        # Performance issue: No pagination, could return massive datasets
        # Performance issue: Inefficient algorithm O(n²)
        all_payments = self._fetch_all_payments()  # Could be millions of records
        user_payments = []

        for payment in all_payments:
            for field in payment:  # Unnecessary nested iteration
                if field == "user_id" and payment[field] == user_id:
                    user_payments.append(payment)
                    break

        return user_payments

    def _fetch_all_payments(self):
        """Simulated method that would fetch all payments"""
        # Maintainability issue: Hard-coded test data
        return [
            {"user_id": 1, "amount": 100, "status": "success"},
            {"user_id": 2, "amount": 200, "status": "failed"},
            {"user_id": 1, "amount": 150, "status": "success"},
        ]
