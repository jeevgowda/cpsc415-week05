def validate_receipt(data):
    items = data.get("items", [])
    subtotal = sum(item.get("price", 0.0) * item.get("quantity", 1) for item in items)
    tax = data.get("tax", 0.0)
    reported_total = data.get("total", 0.0)
    
    calc_total = round(subtotal + tax, 2)
    if abs(calc_total - reported_total) > 0.01:
        return False, f"Arithmetic Mismatch: calculated subtotal ({subtotal}) + tax ({tax}) = {calc_total}, but reported total is {reported_total}"
    return True, "Arithmetic Verified OK"
