import sqlite3

conn = sqlite3.connect("trusted_numbers.db")
c = conn.cursor()

# Recreate or alter table to include times_checked
c.execute("""
CREATE TABLE IF NOT EXISTS trusted_numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    organization TEXT NOT NULL,
    trust_level TEXT NOT NULL,
    times_checked INTEGER DEFAULT 0
)
""")

# Sample data
sample_data = [
    ("1800123456", "Bank of India", "High", 3),
    ("1800456789", "State Bank of India", "Medium", 2),
    ("1800111222", "Reserve Bank of India", "High", 1)
]

c.executemany("INSERT INTO trusted_numbers (number, organization, trust_level, times_checked) VALUES (?, ?, ?, ?)", sample_data)
conn.commit()
conn.close()

print("✅ Database ready with times_checked field.")
