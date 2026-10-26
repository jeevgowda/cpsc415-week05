import unittest

def validate_receipt(data):
    items = data.get("items", [])
    subtotal = sum(item.get("price", 0.0) * item.get("quantity", 1) for item in items)
    tax = data.get("tax", 0.0)
    reported_total = data.get("total", 0.0)
    
    calc_total = round(subtotal + tax, 2)
    if abs(calc_total - reported_total) > 0.01:
        return False, f"Mismatch: calculated {calc_total} vs reported {reported_total}"
    return True, "OK"

class TestChecker(unittest.TestCase):
    def test_valid_arithmetic(self):
        receipt = {
            "items": [{"name": "Coffee", "price": 4.00, "quantity": 2}],
            "tax": 0.80,
            "total": 8.80
        }
        valid, msg = validate_receipt(receipt)
        self.assertTrue(valid)

    def test_invalid_arithmetic(self):
        receipt = {
            "items": [{"name": "Sandwich", "price": 10.00, "quantity": 1}],
            "tax": 1.00,
            "total": 15.00 # Incorrect total
        }
        valid, msg = validate_receipt(receipt)
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()
