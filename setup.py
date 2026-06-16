"""
VeerAI Setup Script — Run this once to install dependencies and initialize DB.
"""
import subprocess
import sys
import os

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

print("=" * 60)
print("  VeerAI — Defence Aspirant Chatbot Setup")
print("=" * 60)

# Install dependencies
print("\n📦 Installing dependencies...")
packages = [
    "flask==2.3.3",
    "SQLAlchemy==1.4.46",
    "pytz==2023.3",
]

for pkg in packages:
    run(f"{sys.executable} -m pip install {pkg} -q")

# Try ChatterBot
print("\n🤖 Installing ChatterBot (optional)...")
cb_ok = run(f"{sys.executable} -m pip install chatterbot==1.0.4 chatterbot-corpus==1.2.0 -q")
if not cb_ok:
    print("⚠️  ChatterBot install failed — app will use built-in knowledge base (works fine!)")

# Init DB
print("\n🗄️  Initialising database...")
sys.path.insert(0, os.path.dirname(__file__))
try:
    from modules.database import init_db
    init_db()
    print("✅ Database ready!")
except Exception as e:
    print(f"⚠️  DB init warning: {e}")

print("\n" + "=" * 60)
print("  ✅ Setup complete!")
print("  Run:  python app.py")
print("  Open: http://localhost:5000")
print("=" * 60)
