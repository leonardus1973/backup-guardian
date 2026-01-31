#!/usr/bin/env python3
"""
Script di validazione per Backup Guardian
Verifica che tutti i file necessari siano presenti e corretti
"""

import json
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica che un file esista."""
    if os.path.exists(filepath):
        print(f"✅ {description}: OK")
        return True
    else:
        print(f"❌ {description}: MANCANTE")
        return False

def validate_json(filepath, description):
    """Valida che un file JSON sia corretto."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {description}: JSON valido")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {description}: JSON non valido - {e}")
        return False
    except FileNotFoundError:
        print(f"❌ {description}: File non trovato")
        return False

def main():
    """Esegue la validazione completa."""
    print("🔍 Validazione Backup Guardian Integration\n")
    
    base_path = "custom_components/backup_guardian"
    all_ok = True
    
    # File Python richiesti
    print("📝 Controllo file Python:")
    python_files = [
        (f"{base_path}/__init__.py", "File init"),
        (f"{base_path}/config_flow.py", "Config flow"),
        (f"{base_path}/const.py", "Costanti"),
        (f"{base_path}/coordinator.py", "Coordinator"),
        (f"{base_path}/sensor.py", "Sensori"),
    ]
    
    for filepath, desc in python_files:
        if not check_file_exists(filepath, desc):
            all_ok = False
    
    print("\n📋 Controllo file JSON:")
    # File JSON richiesti
    json_files = [
        (f"{base_path}/manifest.json", "Manifest"),
        (f"{base_path}/strings.json", "Strings"),
        (f"{base_path}/translations/it.json", "Traduzione italiana"),
        ("hacs.json", "HACS config"),
    ]
    
    for filepath, desc in json_files:
        if not validate_json(filepath, desc):
            all_ok = False
    
    print("\n🎨 Controllo file frontend:")
    # File frontend
    frontend_files = [
        (f"{base_path}/www/backup-guardian-card.js", "Lovelace card"),
    ]
    
    for filepath, desc in frontend_files:
        if not check_file_exists(filepath, desc):
            all_ok = False
    
    print("\n📚 Controllo documentazione:")
    # Documentazione
    docs = [
        ("README.md", "README principale"),
        ("GUIDA_RAPIDA.md", "Guida rapida"),
        ("CHANGELOG.md", "Changelog"),
        ("LICENSE", "Licenza"),
        ("CONTRIBUTING.md", "Guida contribuzione"),
    ]
    
    for filepath, desc in docs:
        if not check_file_exists(filepath, desc):
            all_ok = False
    
    # Verifica manifest.json nel dettaglio
    print("\n🔍 Verifica dettagliata manifest.json:")
    try:
        with open(f"{base_path}/manifest.json", 'r') as f:
            manifest = json.load(f)
        
        required_keys = ["domain", "name", "version", "documentation", "issue_tracker"]
        for key in required_keys:
            if key in manifest:
                print(f"✅ Chiave '{key}': presente")
            else:
                print(f"❌ Chiave '{key}': mancante")
                all_ok = False
    except Exception as e:
        print(f"❌ Errore nella lettura del manifest: {e}")
        all_ok = False
    
    # Risultato finale
    print("\n" + "="*50)
    if all_ok:
        print("✅ Validazione completata: TUTTO OK!")
        print("✅ L'integrazione è pronta per essere pubblicata!")
        return 0
    else:
        print("❌ Validazione fallita: controlla gli errori sopra")
        return 1

if __name__ == "__main__":
    sys.exit(main())
