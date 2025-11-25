import pathway as pw
from datetime import timedelta

# Test with the exact same method from the docs
data = pw.debug.table_from_markdown('''
| name             | time                     | chocolate_bars
| Fudge_McChoc     | 2023-06-22 09:15:00      | 4
| Ganache_Gobbler  | 2023-06-22 10:00:00      | 3
| Truffle_Muncher  | 2023-06-22 11:30:00      | 2
| Fudge_McChoc     | 2023-06-22 13:45:00      | 6
| Ganache_Gobbler  | 2023-06-22 14:20:00      | 5
| Truffle_Muncher  | 2023-06-22 16:10:00      | 8
| Fudge_McChoc     | 2023-06-22 17:50:00      | 3
| Ganache_Gobbler  | 2023-06-22 18:30:00      | 5
| Truffle_Muncher  | 2023-06-22 19:05:00      | 3
''')

print("🧪 Testing tumbling window exactly from docs...")
result = data.windowby(
    data.time,
    window=pw.temporal.tumbling(duration=timedelta(hours=5)),
    instance=data.name,
).reduce(
    name=pw.this._pw_instance,
    window_start=pw.this._pw_window_start,
    window_end=pw.this._pw_window_end,
    chocolate_bars=pw.reducers.sum(pw.this.chocolate_bars),
)

pw.debug.compute_and_print(result, include_id=False)
print("✅ Success!")
