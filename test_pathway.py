import pathway as pw

# Test 1: Can we read the CSV?
print("🧪 Test 1: Reading CSV data...")
prices = pw.demo.replay_csv(
    path="data/stream_prices.csv",
    schema=pw.schema_from_csv("data/stream_prices.csv"),
    input_rate=20
)

print("✅ CSV loaded successfully!")
print(f"Schema: {prices.schema}")

# Test 2: Can we output without windowby?
print("\n🧪 Test 2: Writing to output...")
pw.io.jsonlines.write(prices, "data/test_output.jsonl")

print("🚀 Running Pathway...")
pw.run()
print("✅ Success!")
