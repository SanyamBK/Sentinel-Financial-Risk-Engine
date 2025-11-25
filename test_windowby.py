import pathway as pw
from datetime import datetime, timedelta

print("🧪 Creating test data with proper datetime formatting...")

# Create simple test data
test_data = pw.debug.table_from_markdown(
    """
    timestamp           | price
    2025-01-01 00:00:00 | 100.0
    2025-01-01 00:00:01 | 101.0
    2025-01-01 00:00:02 | 102.0
    2025-01-01 00:00:30 | 103.0
    2025-01-01 00:00:31 | 104.0
    2025-01-01 00:01:00 | 105.0
    """
)

print("✅ Test data created")
print(f"Schema: {test_data.schema}")

# Try a simple windowby operation
print("\n🧪 Testing windowby...")

try:
    windowed = test_data.windowby(
        test_data.timestamp,
        window=pw.temporal.tumbling(duration=timedelta(seconds=30)),
        behavior=pw.temporal.common_behavior()
    ).reduce(
        window_end=pw.this._pw_window_end,
        count=pw.reducers.count()
    )
    
    print("✅ Windowby operation successful!")
    pw.debug.compute_and_print(windowed)
    
except Exception as e:
    print(f"❌ Windowby failed: {e}")
    import traceback
    traceback.print_exc()
