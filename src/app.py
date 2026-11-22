#!/usr/bin/env python3
import os
from pathlib import Path
from flask import Flask, request, render_template_string

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Hardened Defense Layers:
# Layer 1: Character level restrictions (no dots, underscores, brackets)
BLOCKED_CHARS = [
    ".",   # Direct attribute access operator
    "_",   # Dunder / private attribute operator
    "[",   # Direct indexing / bracket notation
    "]",   # Direct indexing / bracket notation
]

# Layer 2: Keyword filter (introspection & smuggling keywords)
BLOCKED_KEYWORDS = [
    "class",       # Class introspection
    "mro",         # Method resolution order
    "base",        # Base class
    "subclasses",  # Subclass traversal
    "config",      # Flask config
    "self",        # Template self
    "os",          # OS module
    "popen",       # Process spawning
    "system",      # System call
    "exec",        # Execution builtin
    "eval",        # Evaluation builtin
    "builtins",    # Builtins dictionary
    "globals",     # Globals dictionary
    "request",     # Request smuggling object
    "args",        # Query parameters
    "cookies",     # Cookie storage
    "headers",     # HTTP headers
    "values",      # Combined parameters
    "form",        # Form parameters
    "session",     # Session object
]

# Layer 3: Military telegraph transmission length limit
MAX_DISPATCH_LENGTH = 350

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
    .rules-box { background: #131d19; border: 1px solid #3d5a45; padding: 12px; border-radius: 4px; margin-bottom: 15px; font-size: 12px; color: #a3b18a; }
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
    <p>Tenente Generale Oreste Baratieri &bull; Modulo Ordini Operativi Campali [የባራቲየሪ ድንብርብር]</p>

    <div class="rules-box">
      <strong>NORME DI SICUREZZA TELEGRAFICA CAMPALE:</strong><br>
      &bull; Canale analogico monofrequenza: vietati caratteri speciali (<strong>.</strong>, <strong>_</strong>, <strong>[</strong>, <strong>]</strong>).<br>
      &bull; Divieto di canali di contrabbando (nessun parametro URL o intestazioni ausiliarie).<br>
      &bull; Lunghezza massima dispaccio: 350 caratteri.
    </div>

    {% if alert %}
      <div class="waf-alert">⚠️ ERRORE SICUREZZA: Tentativo di sabotaggio rilevato! Motivo: '{{ alert }}'</div>
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

def inspect_request_security():
    # Layer 4: Smuggling & parameter injection prevention
    if len(request.args) > 0:
        return "Parametri URL non autorizzati nella linea di trasmissione"
    for k in request.form.keys():
        if k != "memo":
            return f"Campo modulo imprevisto: '{k}'"
    return None

def waf_check(user_text: str):
    # Length check
    if len(user_text) > MAX_DISPATCH_LENGTH:
        return f"Dispaccio troppo lungo ({len(user_text)} car.). Limite consentito: {MAX_DISPATCH_LENGTH} caratteri"

    # Character check
    for ch in BLOCKED_CHARS:
        if ch in user_text:
            return f"Carattere vietato: '{ch}'"

    # Keyword check
    lower_text = user_text.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in lower_text:
            return f"Termine proibito: '{kw}'"

    return None

@app.route("/", methods=["GET", "POST"])
def index():
    rendered_output = None
    alert = None
    raw_input = ""

    if request.method == "POST":
        # First verify request channels for smuggling attempts
        channel_violation = inspect_request_security()
        if channel_violation:
            alert = channel_violation
        else:
            raw_input = request.form.get("memo", "")
            detected = waf_check(raw_input)
            if detected:
                alert = detected
            else:
                try:
                    rendered_output = render_template_string(raw_input)
                except Exception as e:
                    rendered_output = f"[Errore di formattazione telegrafica: {e}]"

    return render_template_string(TEMPLATE_PAGE, rendered_output=rendered_output, alert=alert, raw_input=raw_input)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
