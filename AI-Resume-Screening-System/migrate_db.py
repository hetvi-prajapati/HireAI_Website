import sqlite3
import os

# Use the same DB file the app uses (relative to AI-Resume-Screening-System/)
DB_PATH = 'talentsync.db'
if not os.path.exists(DB_PATH):
    DB_PATH = 'app/database/talentsync.db'

print(f'Using DB: {os.path.abspath(DB_PATH)}')
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()
cols = [row[1] for row in cur.execute('PRAGMA table_info(users)').fetchall()]
print(f'Existing columns: {cols}')

if 'is_outlier' not in cols:
    cur.execute('ALTER TABLE users ADD COLUMN is_outlier INTEGER DEFAULT 0')
    print('Added is_outlier column')
else:
    print('is_outlier already exists — skipped')

if 'cluster_label' not in cols:
    cur.execute("ALTER TABLE users ADD COLUMN cluster_label TEXT DEFAULT 'Unclustered'")
    print('Added cluster_label column')
else:
    print('cluster_label already exists — skipped')

conn.commit()
conn.close()
print('Migration complete. Zero rows deleted.')
