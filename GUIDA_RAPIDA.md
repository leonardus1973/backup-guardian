# 🚀 Guida Rapida - Backup Guardian

## Installazione in 3 Passi

### 📥 Passo 1: Installa l'Integrazione

**Opzione A - Via HACS (Consigliato)**
1. Apri HACS in Home Assistant
2. Vai su "Integrazioni"
3. Clicca sui 3 puntini → "Repository personalizzati"
4. Aggiungi: `https://github.com/leonardus1973/backup-guardian`
5. Categoria: "Integration"
6. Installa "Backup Guardian"
7. **RIAVVIA HOME ASSISTANT**

**Opzione B - Manuale**
1. Scarica la cartella `custom_components/backup_guardian`
2. Copiala in `config/custom_components/backup_guardian/`
3. **RIAVVIA HOME ASSISTANT**

### ⚙️ Passo 2: Configura l'Integrazione

1. Vai su **Impostazioni** → **Dispositivi e Servizi**
2. Clicca **+ Aggiungi Integrazione**
3. Cerca "Backup Guardian"
4. Clicca "Invia"

✅ Fatto! I sensori sono ora attivi.

### 🎨 Passo 3: Aggiungi la Card alla Dashboard

#### A. Registra la Risorsa JavaScript (PRIMA VOLTA)

1. Vai su **Impostazioni** → **Dashboard** → **Risorse**
2. Clicca **+ Aggiungi risorsa**
3. URL: `/local/community/backup_guardian/backup-guardian-card.js`
4. Tipo: **Modulo JavaScript**
5. Clicca **Crea**

**OPPURE** aggiungi a `configuration.yaml`:
```yaml
lovelace:
  resources:
    - url: /local/community/backup_guardian/backup-guardian-card.js
      type: module
```

#### B. Aggiungi la Card

1. Entra in modalità modifica dashboard
2. **+ Aggiungi Card**
3. Scorri in basso → **Personalizzata: Backup Guardian Card**
4. Inserisci:

```yaml
type: custom:backup-guardian-card
entity: sensor.totale_backup
last_backup_entity: sensor.ultimo_backup
```

5. Salva!

## 📊 Cosa Otterrai

### 3 Sensori Automatici

1. **sensor.ultimo_backup** - Data/ora ultimo backup
2. **sensor.totale_backup** - Numero totale backup
3. **sensor.dimensione_totale_backup** - Spazio occupato (MB)

### 1 Card Interattiva

- 📦 Info ultimo backup (nome, data, ora, dimensione, hash)
- 🔘 Bottone con totale backup
- 📋 Clic → lista completa di tutti i backup

## 🎯 Esempi di Uso

### Automazione: Notifica se nessun backup recente

```yaml
automation:
  - alias: "Avviso Backup Mancante"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: template
        value_template: >
          {{ (now() - states.sensor.ultimo_backup.last_changed).days > 7 }}
    action:
      - service: notify.mobile_app
        data:
          message: "⚠️ Nessun backup da più di 7 giorni!"
```

### Script: Pulizia Backup Vecchi

```yaml
script:
  cleanup_old_backups:
    sequence:
      - service: backup.delete
        data:
          # Configura secondo necessità
```

## 🛠️ Personalizzazione

### Cambia Intervallo Aggiornamento

Modifica `custom_components/backup_guardian/const.py`:
```python
UPDATE_INTERVAL = 300  # 5 minuti (default)
# Cambia a 600 per 10 minuti, 60 per 1 minuto, ecc.
```

## ❓ Problemi Comuni

**La card non appare?**
- Svuota cache browser (Ctrl+F5)
- Verifica risorsa JavaScript registrata
- Riavvia Home Assistant

**Nessun backup trovato?**
- Verifica che ci siano file `.tar` in `/backup`
- Controlla log: Impostazioni → Sistema → Log

**Sensori non creati?**
- Verifica installazione corretta
- Riavvia Home Assistant
- Controlla configurazione integrazione

## 📞 Supporto

- 🐛 Bug? Apri un [Issue su GitHub](https://github.com/leonardus1973/backup-guardian/issues)
- 💡 Idee? Apri una [Feature Request](https://github.com/leonardus1973/backup-guardian/issues)
- ⭐ Ti piace? Lascia una stella!

---

**Buon monitoraggio! 🛡️**
