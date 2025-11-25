import pathway as pw

print("Checking Pathway API...")
print(f"Version: {pw.__version__}")

print("\nTop level pw attributes:")
print([x for x in dir(pw) if 'join' in x])

# Create a dummy table to check methods
t = pw.debug.table_from_markdown('''
| col
| 1
''')

print("\nTable attributes:")
print([x for x in dir(t) if 'join' in x])
print([x for x in dir(t) if 'window' in x])
