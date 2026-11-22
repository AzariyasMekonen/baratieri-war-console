#!/usr/bin/env python3
import os
from pathlib import Path
from flask import Flask, request, render_template_string

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Hardened Defense Layers:
# Layer 1: Character level restrictions
BLOCKED_CHARS = [
    ".",   # Direct attribute access operator
    "_",   # Dunder / private attribute operator
    "[",   # Direct indexing / bracket notation
    "]",   # Direct indexing / bracket notation
]

# Layer 2: Keyword filter
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

# Layer 3: Telegraph dispatch length limit
MAX_DISPATCH_LENGTH = 350

TEMPLATE_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Regio Esercito Italiano &bull; Console Telegrafica Campale</title>
  <style>
    :root {
      --bg-dark: #0f1412;
      --panel-bg: #151d1a;
      --brass: #c89f56;
      --brass-bright: #e5be78;
      --brass-dark: #8c6a30;
      --ink: #e0e4dc;
      --border: #2e3d36;
      --alert-bg: #4a1515;
      --alert-border: #d93838;
      --alert-text: #ffd6d6;
      --telegram-paper: #e9e2ce;
      --telegram-ink: #161e1b;
      --status-green: #4ade80;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(ellipse at top, #1b2823 0%, #0d1210 70%),
        repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 0, 0, 0.25) 2px, rgba(0, 0, 0, 0.25) 4px);
      color: var(--ink);
      font-family: 'Courier New', Courier, monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 30px 15px;
    }

    .container {
      width: 100%;
      max-width: 860px;
      background: var(--panel-bg);
      border: 2px solid var(--brass-dark);
      border-radius: 8px;
      box-shadow: 
        0 0 0 1px #050807,
        0 15px 40px rgba(0, 0, 0, 0.85),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
      overflow: hidden;
      position: relative;
    }

    .header-bar {
      background: linear-gradient(180deg, #1f2c26 0%, #17211d 100%);
      border-bottom: 2px solid var(--brass-dark);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      letter-spacing: 1px;
      color: #9cb0a4;
    }

    .status-indicator {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      background: var(--status-green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--status-green);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% { opacity: 0.7; }
      50% { opacity: 1; filter: drop-shadow(0 0 6px var(--status-green)); }
      100% { opacity: 0.7; }
    }

    .main-body {
      padding: 30px;
    }

    .title-section {
      border-bottom: 1px solid var(--border);
      padding-bottom: 18px;
      margin-bottom: 24px;
    }

    h1 {
      font-size: 20px;
      color: var(--brass-bright);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      font-weight: bold;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    .subtitle {
      font-size: 12px;
      color: #8fa196;
      margin-top: 6px;
      letter-spacing: 0.5px;
    }

    .amharic-tag {
      color: var(--brass);
      font-weight: bold;
    }

    .alert-banner {
      background: var(--alert-bg);
      border: 1px solid var(--alert-border);
      border-left: 5px solid var(--alert-border);
      color: var(--alert-text);
      padding: 14px 18px;
      border-radius: 4px;
      margin-bottom: 24px;
      font-size: 13px;
      line-height: 1.4;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }

    .form-group {
      margin-bottom: 22px;
    }

    label {
      display: block;
      font-size: 12px;
      color: var(--brass);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
      font-weight: bold;
    }

    textarea {
      width: 100%;
      height: 120px;
      background: #0d1210;
      color: #b8c7be;
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 14px;
      font-family: 'Courier New', Courier, monospace;
      font-size: 14px;
      line-height: 1.5;
      resize: vertical;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    textarea:focus {
      outline: none;
      border-color: var(--brass);
      box-shadow: 0 0 10px rgba(200, 159, 86, 0.2);
    }

    .action-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 15px;
    }

    button {
      background: linear-gradient(180deg, var(--brass-bright) 0%, var(--brass) 100%);
      color: #0b0f0d;
      border: 1px solid #e5be78;
      border-radius: 4px;
      padding: 12px 28px;
      font-family: inherit;
      font-size: 13px;
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: 1px;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.4);
      transition: all 0.2s;
    }

    button:hover {
      background: linear-gradient(180deg, #f0cf90 0%, var(--brass-bright) 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(200, 159, 86, 0.35);
    }

    button:active {
      transform: translateY(1px);
      box-shadow: 0 2px 6px rgba(0,0,0,0.6);
    }

    .telegram-dispatch {
      margin-top: 30px;
      background: var(--telegram-paper);
      color: var(--telegram-ink);
      border: 1px solid #baa984;
      border-radius: 4px;
      padding: 22px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.6);
      position: relative;
    }

    .telegram-dispatch::before {
      content: "TELEGRAMMA UFFICIALE &bull; STATO MAGGIORE";
      display: block;
      font-size: 10px;
      font-weight: bold;
      letter-spacing: 2px;
      color: #61553c;
      border-bottom: 2px solid #61553c;
      padding-bottom: 8px;
      margin-bottom: 14px;
    }

    .telegram-content {
      font-size: 15px;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
      font-weight: 600;
    }

    .telegram-footer {
      margin-top: 16px;
      padding-top: 10px;
      border-top: 1px dashed #baa984;
      font-size: 10px;
      color: #7d6e50;
      display: flex;
      justify-content: space-between;
    }

    .footer-stamp {
      background: #0f1412;
      border-top: 1px solid var(--border);
      padding: 14px 24px;
      font-size: 10px;
      color: #6a7c72;
      text-align: center;
      letter-spacing: 1px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header-bar">
      <div class="status-indicator">
        <span class="status-dot"></span>
        <span>LINEA DI TRASMISSIONE SAURIA &bull; ADUA</span>
      </div>
      <div>29 FEBBRAIO 1896 &bull; ORE 23:45</div>
    </div>

    <div class="main-body">
      <div class="title-section">
        <h1>Console Telegrafica Campale</h1>
        <div class="subtitle">
          Quartier Generale di Sauria &bull; Tenente Generale Oreste Baratieri
        </div>
      </div>

      {% if alert %}
        <div class="alert-banner">
          <span>⚠️</span>
          <span><strong>ERRORE TRASMISSIONE:</strong> {{ alert }}</span>
        </div>
      {% endif %}

      <form method="POST" action="/">
        <div class="form-group">
          <label for="memo">Bozza Ordine del Giorno / Rapporto Operativo:</label>
          <textarea id="memo" name="memo" placeholder="Comporre dispaccio per le brigate (es. Avanzata Colonna Albertone ore 04:00 verso il colle di Kidane Mehret)...">{{ raw_input }}</textarea>
        </div>

        <div class="action-row">
          <button type="submit">Trasmetti Dispaccio Telegrafico</button>
        </div>
      </form>

      {% if rendered_output is not none %}
        <div class="telegram-dispatch">
          <div class="telegram-content">{{ rendered_output }}</div>
          <div class="telegram-footer">
            <span>REGIO CORPO TRUPPE COLONIALI</span>
            <span>RICEVUTO E ARCHIVIATO AI POSTI DI BRIGATA</span>
          </div>
        </div>
      {% endif %}
    </div>

    <div class="footer-stamp">
      SEZIONE TELEGRAFICA MILITARE &bull; CIFRARIO RISERVATO DEL COMANDO SUPREMO D'AFRICA
    </div>
  </div>
</body>
</html>
"""

def inspect_request_security():
    # Layer 4: Smuggling & parameter injection prevention
    if len(request.args) > 0:
        return "Canale di trasmissione compromesso (parametri URL non autorizzati)"
    for k in request.form.keys():
        if k != "memo":
            return "Segnale telegrafico anomalo (campi modulo non riconosciuti)"
    return None

def waf_check(user_text: str):
    # Length check
    if len(user_text) > MAX_DISPATCH_LENGTH:
        return "Capacità massima della linea telegrafica campale superata"

    # Character check
    for ch in BLOCKED_CHARS:
        if ch in user_text:
            return "Interferenza di linea: carattere non ammesso dal protocollo telegrafico"

    # Keyword check
    lower_text = user_text.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in lower_text:
            return "Censura militare: termine non ammesso negli ordini di brigata"

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
                    rendered_output = f"[Errore linea telegrafica: {e}]"

    return render_template_string(TEMPLATE_PAGE, rendered_output=rendered_output, alert=alert, raw_input=raw_input)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
