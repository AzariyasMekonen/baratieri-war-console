#!/usr/bin/env python3
import os
from pathlib import Path
from flask import Flask, request, render_template_string

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Italian Headquarters WAF Filter
BLOCKED_KEYWORDS = [
    "__",          # Double underscore
    "class",       # Class introspection keyword
    "mro",         # Method Resolution Order
    "base",        # Base class keyword
    "subclasses",  # Subclass traversal
    "config",      # Flask config object
    "self",        # Template self reference
    "os",          # OS module
    "popen",       # Process spawning
    "system",      # System command
]

TEMPLATE_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Regio Esercito Italiano - Console Telegrafica Campale</title>
  <style>
    body { background-color: #1c2321; color: #e0e2db; font-family: 'Courier New', monospace; padding: 25px; }
    .terminal { max-width: 850px; margin: 0 auto; background: #0b0f0e; border: 2px solid #5e6572; border-radius: 6px; padding: 25px; box-shadow: 0 0 20px rgba(0,0,0,0.8); }
    h1 { color: #d4a373; font-size: 20px; border-bottom: 1px dashed #5e6572; padding-bottom: 10px; }
    .waf-alert { background: #5c1d1d; color: #ffcccc; padding: 12px; border: 1px solid #ff4d4d; border-radius: 4px; margin-bottom: 20px; font-weight: bold; }
    textarea { width: 100%; height: 120px; background: #18231f; color: #a3b18a; border: 1px solid #5e6572; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 14px; box-sizing: border-box; }
    button { background: #d4a373; color: #0b0f0e; border: none; padding: 10px 20px; font-weight: bold; margin-top: 10px; cursor: pointer; border-radius: 4px; }
    button:hover { background: #faedcd; }
    .dispatch-view { margin-top: 25px; padding: 15px; background: #141f1b; border-left: 4px solid #d4a373; border-radius: 2px; }
    .stamp { font-size: 11px; color: #7f9183; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="terminal">
    <h1>TELEGRAFO MILITARE - QUARTIER GENERALE DI SAURIA (ADUA 1896)</h1>
    <p>Tenente Generale Oreste Baratieri &bull; Modulo Ordini Operativi Campali</p>

    {% if alert %}
      <div class="waf-alert">⚠️ ERRORE SICUREZZA: Tentativo di sabotaggio rilevato! Parola chiave vietata: '{{ alert }}'</div>
    {% endif %}

    <form method="POST" action="/">
      <label for="memo">Bozza Ordine del Giorno / Rapporto di Marcia:</label><br>
      <textarea id="memo" name="memo" placeholder="Inserire messaggio telegrafico (es: Avanzata Colonna Albertone ore 04:00)...">{{ raw_input }}</textarea><br>
      <button type="submit">Trasmetti Dispaccio Telegrafico</button>
    </form>

    {% if rendered_output is not none %}
      <div class="dispatch-view">
        <strong>DISPACCIO TRASMESSO AGLI UFFICIALI DI BRIGATA:</strong>
        <pre>{{ rendered_output }}</pre>
      </div>
    {% endif %}

    <div class="stamp">
      SISTEMA DI CIFRATURA AUTOMATICA - STATO MAGGIORE DEL REGIO CORPO TRUPPE COLONIALI
    </div>
  </div>
</body>
</html>
"""

def waf_check(user_text: str):
    lower_text = user_text.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in lower_text:
            return kw
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    rendered_output = None
    alert = None
    raw_input = ""

    if request.method == "POST":
        raw_input = request.form.get("memo", "")
        # Inspect for malicious patterns
        detected = waf_check(raw_input)
        if detected:
            alert = detected
        else:
            try:
                # Render via Jinja2 engine
                rendered_output = render_template_string(raw_input)
            except Exception as e:
                rendered_output = f"[Errore di formattazione telegrafica: {e}]"

    return render_template_string(TEMPLATE_PAGE, rendered_output=rendered_output, alert=alert, raw_input=raw_input)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)

