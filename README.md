# Debugpy Demo — VS Code Remote Debugging Tutorial

Interactive tutorial demonstrating VS Code remote debugging features using debugpy.

## Prerequisites

- **Server**: Python 3 with debugpy installed (already in `venv/`)
- **Laptop**: VS Code with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Network connectivity between laptop and server on port 5678

## Quick Start

### 1. Start the demo on the server

```bash
cd /mnt/samsung_ssd/development/debugpy_demo
venv/bin/python demo_debugpy.py
```

The script will print instructions and wait for a debugger to attach.

### 2. Configure VS Code on your laptop

Add this to your `.vscode/launch.json` (create the file if it doesn't exist):

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "YOUR_SERVER_IP",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/mnt/samsung_ssd/development/debugpy_demo"
                }
            ],
            "justMyCode": true
        }
    ]
}
```

Replace `YOUR_SERVER_IP` with your server's IP address.

### 3. Attach the debugger

1. Open the Run & Debug panel (**Ctrl+Shift+D**)
2. Select **"Python: Remote Attach"** from the dropdown
3. Press **F5** (or click the green play button)
4. The script will resume — follow the on-screen prompts

## Section-by-Section Walkthrough

### Section 1: Remote Debugging Setup

**What happens:** The script calls `debugpy.listen()` and `debugpy.wait_for_client()`.

**What to show:**
- The script is running on the server but we're debugging from our laptop
- Once attached, the debug toolbar appears in VS Code (continue, step, stop, etc.)

---

### Section 2: Basic Breakpoints & Variable Inspection

**What happens:** A function creates nested data structures (dict, list, matrix).

**What to demo:**
- Click in the gutter (left of line numbers) to set a breakpoint on the first line inside `explore_variables()`
- When the breakpoint hits, expand the **Variables** panel in the sidebar
- Expand `user` → show nested `address` dict and `roles` list
- Expand `matrix` → show the list of lists
- Hover over `average` to see its value inline

---

### Section 3: Stepping Through Code

**What happens:** `calculate_total()` calls `apply_discount()` then `apply_tax()`.

**What to demo:**
- Set a breakpoint on the `result = calculate_total(...)` line
- **Step In** (F11) → enters `calculate_total`, then step in again to enter `apply_discount`
- **Step Out** (Shift+F11) → returns to `calculate_total`
- **Step Over** (F10) → runs `apply_tax` without entering it
- Watch the **Call Stack** panel as you step in and out

---

### Section 4: Conditional Breakpoints

**What happens:** A loop iterates over 8 catalog items.

**What to demo:**
- Set a breakpoint inside the `for` loop
- Right-click the breakpoint → **Edit Breakpoint...** → **Expression**
- Enter: `item["id"] == 5` → debugger only pauses on item #5
- Try: `item["price"] > 100` → pauses on items over $100
- Try: `"Pro" in item["name"]` → pauses on "Pro" items

---

### Section 5: Exception Breakpoints

**What happens:** Three different exceptions are raised and caught.

**What to demo:**
- In the **Breakpoints** panel (bottom of Run & Debug sidebar):
  - Check **"Raised Exceptions"** → debugger pauses on every exception, even caught ones
  - Uncheck it and check **"Uncaught Exceptions"** → debugger does NOT pause (all are caught)
- Show how you can filter which exception types to break on

---

### Section 6: Programmatic Breakpoints

**What happens:** `debugpy.breakpoint()` is called inside `process_order()` when the subtotal exceeds $500.

**What to demo:**
- No IDE breakpoint needed — the code itself triggers the pause
- The first order (small) runs normally
- The second order (large, >$500) triggers `debugpy.breakpoint()` and pauses
- Inspect `subtotal`, `order_id`, and `items` in the Variables panel
- Explain use cases: conditional breaks in code, shareable via source control

---

### Section 7: Logpoints

**What happens:** Data is processed in batches with a small delay.

**What to demo:**
- Instead of a regular breakpoint, right-click the gutter → **Add Logpoint...**
- Enter a message: `Batch {batch_id}: items={batch}, progress={pct:.0%}`
- The logpoint shows as a diamond (◆) instead of a circle
- Run the code — messages appear in the **Debug Console** without pausing
- Compare to print debugging: no code changes needed, easily toggled

---

### Section 8: Multi-threaded Debugging

**What happens:** Three threads run concurrently (Downloader, Processor, Uploader).

**What to demo:**
- Set a breakpoint inside `worker()` on the `status = ...` line
- When a thread hits the breakpoint, open the **Call Stack** panel
- You'll see all three threads listed — click each to switch context
- Each thread has its own call stack, locals, and `name`/`step` values
- Use **Continue** (F5) to let one thread advance, observe others pausing

---

### Section 9: Watch Expressions & Debug Console

**What happens:** 10 transactions are processed, accumulating a running total.

**What to demo:**
- Set a breakpoint inside the loop on the `status = ...` line
- In the **Watch** panel (click the + button), add:
  - `running_total`
  - `len(history)`
  - `max(history) if history else 0`
  - `running_total / len(history)`
- Watch values update as you step through iterations
- Open the **Debug Console** (bottom panel) and type expressions:
  - `history[-3:]` — last 3 running totals
  - `[h for h in history if h > 100]` — filter history
  - `import math; math.sqrt(running_total)` — arbitrary Python

## VS Code Debug Features Quick Reference

| Feature | How to Access | Description |
|---|---|---|
| **Breakpoint** | Click gutter (left of line number) | Pause execution at this line |
| **Conditional Breakpoint** | Right-click gutter → Edit Breakpoint → Expression | Pause only when condition is true |
| **Hit Count Breakpoint** | Right-click gutter → Edit Breakpoint → Hit Count | Pause after N hits |
| **Logpoint** | Right-click gutter → Add Logpoint | Log a message without pausing |
| **Exception Breakpoints** | Breakpoints panel → checkboxes | Pause on raised/uncaught exceptions |
| **Step Over** | F10 | Run current line, skip function internals |
| **Step In** | F11 | Enter the function being called |
| **Step Out** | Shift+F11 | Finish current function, return to caller |
| **Continue** | F5 | Resume until next breakpoint |
| **Watch Expression** | Watch panel → + button | Evaluate an expression at each pause |
| **Debug Console** | Bottom panel during debug | Run arbitrary Python in current frame |

## Troubleshooting

**Can't connect to the debugger?**
- Ensure port 5678 is open on the server firewall: `sudo ufw allow 5678/tcp`
- Verify the server IP in `launch.json` matches the server's actual IP
- Check that the script is running and shows "debugpy is now listening..."

**Breakpoints aren't hitting?**
- Ensure `pathMappings` in `launch.json` matches the actual paths
- Check that `justMyCode` is set to `true` (or `false` to debug library code too)
- Make sure you opened the same project folder that's in `localRoot`

**Variables show as "not available"?**
- You may be in optimized code — try setting `"justMyCode": false`
- Ensure you're paused at a breakpoint (not just stopped)
