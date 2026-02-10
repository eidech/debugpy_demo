"""
Debugpy Demo — Interactive tutorial for VS Code remote debugging with debugpy.

Run on your server:
    venv/bin/python demo_debugpy.py

Then attach from VS Code using the remote attach configuration in README.md.
Each section pauses so the presenter controls pacing.
"""

import debugpy
import threading
import time

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def banner(section_number, title):
    """Print a visible section banner."""
    width = 70
    print("\n" + "=" * width)
    print(f"  Section {section_number}: {title}")
    print("=" * width + "\n")


def pause():
    """Wait for the presenter to press Enter before continuing."""
    input("\n>>> Press Enter to continue to the next section...\n")


# ═══════════════════════════════════════════════════════════════════════════════
# Section 1: Remote Debugging Setup
# ═══════════════════════════════════════════════════════════════════════════════

banner(1, "Remote Debugging Setup")

print("Starting debugpy listener on 0.0.0.0:5678 ...")
debugpy.listen(("0.0.0.0", 5678))

print("""
debugpy is now listening for a VS Code attach on port 5678.

  In VS Code on your laptop:
    1. Open the Run & Debug panel (Ctrl+Shift+D)
    2. Select the "Python: Remote Attach" configuration
    3. Click the green ▶ play button (or press F5)

  The script will resume once the debugger is attached.
""")

debugpy.wait_for_client()
print("Debugger attached! Let's begin the demo.\n")

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 2: Basic Breakpoints & Variable Inspection
# ═══════════════════════════════════════════════════════════════════════════════

banner(2, "Basic Breakpoints & Variable Inspection")

print("""Demo: Set a breakpoint on the first line inside `explore_variables()`,
then inspect the local variables in the VS Code Variables panel.

Tip: Expand nested structures (dict, list) in the Variables panel.
""")


def explore_variables():
    # ← SET A BREAKPOINT HERE and inspect the locals below
    user = {
        "name": "Alice",
        "age": 30,
        "roles": ["admin", "editor"],
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
        },
    }

    scores = [85, 92, 78, 95, 88]
    average = sum(scores) / len(scores)

    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    message = f"{user['name']} has an average score of {average:.1f}"
    print(f"  Result: {message}")
    return message


explore_variables()

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 3: Stepping Through Code
# ═══════════════════════════════════════════════════════════════════════════════

banner(3, "Stepping Through Code (Step In / Step Over / Step Out)")

print("""Demo: Set a breakpoint on the `calculate_total(...)` call below, then:
  - Step In  (F11)  → enters `calculate_total`, then `apply_discount`, then `apply_tax`
  - Step Over (F10) → runs the function without entering it
  - Step Out (Shift+F11) → finishes the current function and returns to the caller
""")


def apply_discount(price, discount_pct):
    """Apply a percentage discount."""
    discount = price * (discount_pct / 100)
    final = price - discount
    return final


def apply_tax(price, tax_rate):
    """Apply sales tax."""
    tax = price * tax_rate
    total = price + tax
    return total


def calculate_total(base_price, discount_pct=10, tax_rate=0.08):
    """Calculate the final price after discount and tax."""
    discounted = apply_discount(base_price, discount_pct)
    total = apply_tax(discounted, tax_rate)
    return round(total, 2)


# ← SET A BREAKPOINT HERE and practice stepping
result = calculate_total(250.00, discount_pct=15, tax_rate=0.09)
print(f"  Final total: ${result}")

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 4: Conditional Breakpoints
# ═══════════════════════════════════════════════════════════════════════════════

banner(4, "Conditional Breakpoints")

print("""Demo: Set a breakpoint inside the loop below, then right-click it and
choose "Edit Breakpoint..." → "Expression". Try these conditions:

  item["id"] == 5
  item["price"] > 100
  "Pro" in item["name"]

The debugger will only pause when the condition is True.
""")

catalog = [
    {"id": 1, "name": "Widget Basic", "price": 25.00},
    {"id": 2, "name": "Widget Plus", "price": 49.99},
    {"id": 3, "name": "Widget Pro", "price": 149.99},
    {"id": 4, "name": "Gadget Lite", "price": 19.99},
    {"id": 5, "name": "Gadget Pro", "price": 199.99},
    {"id": 6, "name": "Gadget Ultra", "price": 349.99},
    {"id": 7, "name": "Accessory Pack", "price": 9.99},
    {"id": 8, "name": "Premium Bundle", "price": 499.99},
]

for item in catalog:
    # ← SET A CONDITIONAL BREAKPOINT on this line
    label = f"  [{item['id']}] {item['name']:20s} ${item['price']:>8.2f}"
    print(label)

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 5: Exception Breakpoints
# ═══════════════════════════════════════════════════════════════════════════════

banner(5, "Exception Breakpoints")

print("""Demo: In the VS Code Breakpoints panel, toggle:
  ☑ Raised Exceptions   — pauses on ALL exceptions (even caught ones)
  ☑ Uncaught Exceptions  — pauses only on unhandled exceptions

Watch how the debugger behaves differently for each exception below.
""")


def risky_division(a, b):
    """Intentionally raises ZeroDivisionError when b is 0."""
    return a / b


def parse_number(value):
    """Intentionally raises ValueError for non-numeric strings."""
    return int(value)


# --- Caught exception: ZeroDivisionError ---
print("  Attempting division by zero (caught)...")
try:
    result = risky_division(10, 0)
except ZeroDivisionError as e:
    print(f"  Caught ZeroDivisionError: {e}")

# --- Caught exception: ValueError ---
print("  Attempting to parse 'hello' as int (caught)...")
try:
    result = parse_number("hello")
except ValueError as e:
    print(f"  Caught ValueError: {e}")

# --- Caught exception: KeyError ---
print("  Attempting missing dict key (caught)...")
try:
    data = {"a": 1, "b": 2}
    value = data["missing_key"]
except KeyError as e:
    print(f"  Caught KeyError: {e}")

print("\n  All exceptions were caught — no crash.")

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 6: Programmatic Breakpoints
# ═══════════════════════════════════════════════════════════════════════════════

banner(6, "Programmatic Breakpoints (debugpy.breakpoint())")

print("""Demo: The code below uses `debugpy.breakpoint()` to trigger a pause
without needing to set a breakpoint in the IDE. This is useful for:
  - Breaking inside dynamically generated code
  - Breaking on specific conditions in production-like code
  - Sharing breakpoints via source control
""")


def process_order(order_id, items):
    subtotal = sum(item["price"] * item["qty"] for item in items)

    if subtotal > 500:
        # Programmatic breakpoint: pause here for large orders
        debugpy.breakpoint()
        print(f"  ⚠ Large order #{order_id} detected (subtotal: ${subtotal:.2f})")

    tax = subtotal * 0.08
    total = subtotal + tax
    print(f"  Order #{order_id}: subtotal=${subtotal:.2f}, tax=${tax:.2f}, total=${total:.2f}")
    return total


# Small order — will NOT trigger the programmatic breakpoint
process_order(1001, [
    {"name": "Widget", "price": 25.00, "qty": 2},
    {"name": "Gadget", "price": 15.00, "qty": 1},
])

# Large order — WILL trigger the programmatic breakpoint
process_order(1002, [
    {"name": "Premium Bundle", "price": 499.99, "qty": 2},
    {"name": "Accessory Pack", "price": 9.99, "qty": 5},
])

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 7: Logpoints
# ═══════════════════════════════════════════════════════════════════════════════

banner(7, "Logpoints")

print("""Demo: Instead of adding print() statements, use VS Code Logpoints:

  1. Click in the gutter to the left of a line number (where you'd set a breakpoint)
  2. Right-click → "Add Logpoint..."
  3. Enter a log message using {expression} for interpolation, e.g.:
       Processing batch {batch_id}: progress={pct:.0%}

Logpoints print to the Debug Console without pausing execution.
""")


def process_batches(data, batch_size=3):
    """Process data in batches — ideal for logpoints."""
    total = len(data)
    for i in range(0, total, batch_size):
        batch_id = i // batch_size + 1
        batch = data[i:i + batch_size]
        pct = min((i + batch_size) / total, 1.0)

        # ← ADD A LOGPOINT on this line instead of a breakpoint
        # Suggested message: "Batch {batch_id}: items={batch}, progress={pct:.0%}"
        processed = [x ** 2 for x in batch]
        time.sleep(0.3)  # simulate work

    print(f"  Processed {total} items in {batch_id} batches.")


sample_data = list(range(1, 16))
process_batches(sample_data, batch_size=4)

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 8: Multi-threaded Debugging
# ═══════════════════════════════════════════════════════════════════════════════

banner(8, "Multi-threaded Debugging")

print("""Demo: This section spawns 3 worker threads. In VS Code:
  - Open the Call Stack panel to see all threads
  - Click a thread to switch to its call stack
  - Set a breakpoint inside `worker()` — each thread will pause independently
  - Notice the thread name in the Call Stack panel
""")


def worker(name, steps):
    """Simulate a worker doing multi-step processing."""
    for step in range(1, steps + 1):
        # ← SET A BREAKPOINT HERE to observe per-thread pausing
        status = f"  [{name}] Step {step}/{steps}"
        print(status)
        time.sleep(0.5)  # simulate work
    print(f"  [{name}] Done!")


threads = []
for worker_name, steps in [("Downloader", 4), ("Processor", 3), ("Uploader", 5)]:
    t = threading.Thread(target=worker, args=(worker_name, steps), name=worker_name)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n  All threads finished.")

pause()


# ═══════════════════════════════════════════════════════════════════════════════
# Section 9: Watch Expressions & Debug Console
# ═══════════════════════════════════════════════════════════════════════════════

banner(9, "Watch Expressions & Debug Console")

print("""Demo: Set a breakpoint inside the loop below, then:

  Watch Expressions (in the Watch panel, click +):
    - running_total
    - len(history)
    - max(history) if history else 0
    - running_total / len(history)

  Debug Console (bottom panel):
    - Type any Python expression to evaluate it in the current frame
    - Try: history[-3:]
    - Try: [h for h in history if h > 100]
    - Try: import math; math.sqrt(running_total)
""")


def analyze_transactions(transactions):
    """Process transactions — great for watch expressions."""
    running_total = 0
    history = []
    high_value_count = 0

    for i, txn in enumerate(transactions):
        amount = txn["amount"]
        running_total += amount
        history.append(running_total)

        if amount > 100:
            high_value_count += 1

        avg = running_total / (i + 1)
        # ← SET A BREAKPOINT HERE and add watch expressions
        status = f"  Txn {i+1:2d}: ${amount:>8.2f} | Running total: ${running_total:>10.2f} | Avg: ${avg:>8.2f}"
        print(status)

    print(f"\n  Summary: {len(transactions)} transactions, {high_value_count} high-value")
    print(f"  Final total: ${running_total:,.2f}")


transactions = [
    {"id": 1, "amount": 45.00, "desc": "Office supplies"},
    {"id": 2, "amount": 250.00, "desc": "Software license"},
    {"id": 3, "amount": 12.50, "desc": "Coffee"},
    {"id": 4, "amount": 899.99, "desc": "New monitor"},
    {"id": 5, "amount": 34.99, "desc": "Books"},
    {"id": 6, "amount": 150.00, "desc": "Training course"},
    {"id": 7, "amount": 67.50, "desc": "Team lunch"},
    {"id": 8, "amount": 2400.00, "desc": "Server rental"},
    {"id": 9, "amount": 5.99, "desc": "Domain renewal"},
    {"id": 10, "amount": 175.00, "desc": "Conference ticket"},
]

analyze_transactions(transactions)


# ═══════════════════════════════════════════════════════════════════════════════
# Done
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  Demo complete! Disconnect the debugger when ready.")
print("=" * 70 + "\n")
