#!/bin/bash
echo "👑 Waking up The Council of Kings..."

# 1. Gå ind i mappen (juster stien hvis nødvendigt, men dette er standard)
cd ~/CouncilOfKings/sovereign-engine

# 2. Aktiver det virtuelle miljø (VIGTIGT!)
source venv/bin/activate

# 3. Fortæl brugeren at vi er klar
echo "✅ Environment Activated."
echo "🚀 Starting the UI Dashboard..."

# 4. Start programmet (Vi skifter til dashboard.py om lidt)
python3 final_run.py
