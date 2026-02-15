# 📁 Struttura del Progetto - Backup Guardian v1.1.0

Questo documento descrive la struttura completa del repository e la funzione di ogni file.

## 🗂️ Struttura Directory

```
backup-guardian/
├── custom_components/
│   └── backup_guardian/
│       ├── translations/
│       │   └── it.json
│       ├── www/
│       │   └── backup-guardian-card.js
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── manifest.json
│       ├── sensor.py
│       ├── strings.json
│       ├── icon.png
│       └── logo.png
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ESEMPI_CONFIGURAZIONE.md
├── GUIDA_RAPIDA.md
├── INSTALLATION.md
├── LICENSE
├── QUICK_START.txt
├── README.md
├── STRUCTURE.md
├── hacs.json
├── info.md
└── validate.py
```

---

## 📄 Descrizione File Principali

### 🔧 Core Integration Files

#### `custom_components/backup_guardian/__init__.py`
**Funzione**: Entry point dell'integrazione
- Gestisce setup e unload dell'integrazione
- **Copia automaticamente** il file JavaScript della card in `/config/www/community/`
- Inizializza il coordinator
- Gestisce il ciclo di vita dell'integrazione

**Novità v1.1.0**: Funzione `_copy_frontend_files()` per copia automatica card!

#### `custom_components/backup_guardian/config_flow.py`
**Funzione**: Gestione configurazione tramite UI
- Config flow per aggiunta integrazione da interfaccia
- Validazione configurazione
- Nessuna configurazione richiesta dall'utente (zero-config!)

#### `custom_components/backup_guardian/const.py`
**Funzione**: Costanti dell'integrazione
- `DOMAIN`: Nome dominio integrazione
- `PLATFORMS`: Piattaforme supportate (sensor)
- `UPDATE_INTERVAL`: Intervallo aggiornamento (300s = 5 min)
- Attributi sensori:
  - `ATTR_BACKUP_NAME`
  - `ATTR_BACKUP_DATE`
  - `ATTR_BACKUP_TIME`
  - `ATTR_BACKUP_SIZE`
  - `ATTR_BACKUP_HASH`
  - `ATTR_BACKUP_TYPE`
  - `ATTR_BACKUP_SLUG`
  - `ATTR_BACKUP_LIST`
  - `ATTR_BACKUP_DESTINATION` **[NUOVO v1.1.0]**

#### `custom_components/backup_guardian/coordinator.py`
**Funzione**: Data coordinator per aggiornamento dati
- Connessione a Supervisor API tramite `hassio` component
- Recupero lista backup via `/backups` endpoint
- Conversione date UTC → timezone locale **[FIX v1.1.0]**
- Calcolo dimensioni corrette (bytes → MB)
- Assegnazione destinazione backup (local, google_drive, ecc.) **[NUOVO v1.1.0]**
- Aggiornamento automatico ogni 5 minuti
- Gestione errori robusta

**Funzioni principali**:
- `_get_backups_from_supervisor()`: Recupera backup da API
- `_process_backup(backup_data, source)`: Processa singolo backup con timezone e destinazione
- `_async_update_data()`: Update loop principale

#### `custom_components/backup_guardian/sensor.py`
**Funzione**: Definizione sensori
- Auto-read versione da `manifest.json`
- 3 sensori:
  1. **Ultimo Backup**: Data/ora ultimo backup (con timezone locale)
  2. **Totale Backup**: Numero backup disponibili
  3. **Dimensione Totale**: Spazio occupato in MB

**Attributi sensori**:
- Ultimo backup: nome, data, ora, dimensione, hash, tipo, **destinazione** **[NUOVO v1.1.0]**
- Totale backup: lista completa con **destinazione per ogni backup** **[NUOVO v1.1.0]**

#### `custom_components/backup_guardian/manifest.json`
**Funzione**: Metadati integrazione
```json
{
  "domain": "backup_guardian",
  "name": "Backup Guardian",
  "version": "1.1.0",
  "integration_type": "service",
  "iot_class": "local_polling",
  "icon": "icon.png",
  "logo": "logo.png",
  ...
}
```

#### `custom_components/backup_guardian/strings.json`
**Funzione**: Stringhe UI in inglese (fallback)
- Titoli config flow
- Messaggi di errore
- Descrizioni

#### `custom_components/backup_guardian/translations/it.json`
**Funzione**: Traduzioni italiane complete
- Interfaccia utente in italiano
- Messaggi config flow
- Descrizioni sensori

---

### 🎨 Frontend Files

#### `custom_components/backup_guardian/www/backup-guardian-card.js`
**Funzione**: Custom Lovelace card
- Web Component per visualizzazione backup
- **Badge destinazione colorati** per ogni backup **[NUOVO v1.1.0]**
- Lista espandibile backup
- Design responsive integrato con tema HA
- Statistiche visuali (totale backup, MB)

**Viene copiato automaticamente** da `__init__.py` in:
```
/config/www/community/backup_guardian/backup-guardian-card.js
```

**Caratteristiche**:
- Shadow DOM per isolamento CSS
- Emoji invece di `ha-icon` (no dipendenze)
- Badge `destination-badge` per destinazione backup
- Animazioni espansione lista
- Console log: `✅ Backup Guardian Card loaded successfully!`

#### `custom_components/backup_guardian/icon.png`
**Funzione**: Icona integrazione (256x256 PNG con trasparenza)
- Visualizzata in lista integrazioni
- Badge blu con checkmark e testo "BACKUP GUARDIAN"

#### `custom_components/backup_guardian/logo.png`
**Funzione**: Logo integrazione (256x256 PNG con trasparenza)
- Visualizzato nei dettagli integrazione
- Identico a icon.png

---

### 📚 Documentazione

#### `README.md`
**Funzione**: Documentazione principale completa
- Panoramica integrazione
- Feature list completa
- Guida installazione (HACS + Manuale)
- Configurazione passo-passo
- Descrizione sensori e attributi
- Esempi automazioni
- Troubleshooting esteso
- FAQ

**Aggiornato v1.1.0**: Documentazione copia automatica file JS, badge destinazione, fix timezone

#### `INSTALLATION.md`
**Funzione**: Guida installazione dettagliata
- Prerequisiti
- Installazione HACS step-by-step
- Installazione manuale
- Configurazione Lovelace card completa
- Verifica installazione
- Troubleshooting per ogni step

**Aggiornato v1.1.0**: Nuove istruzioni copia automatica, gestione cache browser

#### `GUIDA_RAPIDA.md`
**Funzione**: Quick start in italiano
- Installazione in 3 passi
- Configurazione base
- Esempi automazioni veloci
- Problemi comuni + soluzioni

**Aggiornato v1.1.0**: Procedura semplificata con auto-copy

#### `ESEMPI_CONFIGURAZIONE.md`
**Funzione**: Esempi pratici di configurazione
- 6+ automazioni pronte all'uso
- Card personalizzate
- Template sensor avanzati
- Script utili
- Dashboard complete

**Aggiornato v1.1.0**: Esempi con attributo `backup_destination`

#### `CHANGELOG.md`
**Funzione**: Storia di tutte le versioni
- Modifiche per ogni release
- Bug fix documentati
- Feature aggiunte
- Breaking changes

**Aggiornato v1.1.0**: Storia completa 1.0.0 → 1.1.0

#### `QUICK_START.txt`
**Funzione**: Quick reference testuale
- Guida rapida formato testo
- Comandi e configurazioni copy-paste
- Troubleshooting veloce

**Aggiornato v1.1.0**: Novità v1.1.0, nuove procedure

#### `STRUCTURE.md` (questo file)
**Funzione**: Documentazione struttura progetto
- Organizzazione directory
- Descrizione ogni file
- Relazioni tra componenti

---

### 🔧 Configuration Files

#### `hacs.json`
**Funzione**: Configurazione HACS
```json
{
  "name": "Backup Guardian",
  "content_in_root": false,
  "filename": "backup_guardian",
  "render_readme": true,
  "homeassistant": "2023.1.0"
}
```

#### `info.md`
**Funzione**: Info breve per HACS store
- Descrizione concisa
- Feature principali
- Istruzioni installazione rapide
- Link documentazione completa

**Aggiornato v1.1.0**: Novità v1.1.0 in evidenza

---

### 📋 Altri Files

#### `CONTRIBUTING.md`
**Funzione**: Guidelines per contributi
- Come contribuire
- Code style
- Pull request process
- Reporting bugs

#### `LICENSE`
**Funzione**: Licenza progetto
- CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial)
- Uso libero ma non commerciale

#### `validate.py`
**Funzione**: Script validazione
- Verifica struttura file
- Controllo sintassi
- Validazione manifest.json

---

## 🔄 Flusso Operativo

### Al Primo Avvio (o Aggiornamento)

1. **`__init__.py`** viene eseguito
2. Funzione `_copy_frontend_files()` copia automaticamente:
   - Da: `/config/custom_components/backup_guardian/www/backup-guardian-card.js`
   - A: `/config/www/community/backup_guardian/backup-guardian-card.js`
3. Viene inizializzato il **coordinator**
4. Il coordinator chiama Supervisor API per recuperare backup

### Durante il Funzionamento

1. **Coordinator** aggiorna dati ogni 5 minuti
2. Recupera lista backup da `/backups` endpoint
3. Processa ogni backup:
   - Converte date UTC → locale
   - Calcola dimensioni bytes → MB
   - Assegna destinazione (local/cloud)
   - Calcola hash SHA256
4. **Sensori** si aggiornano con nuovi dati
5. **Card** visualizza dati con badge destinazione

### Quando l'Utente Apre la Dashboard

1. Browser carica `/local/community/backup_guardian/backup-guardian-card.js`
2. Script definisce custom element `<backup-guardian-card>`
3. Card si connette ai sensori via `hass` object
4. Renderizza UI con badge destinazione

---

## 📊 Dati Gestiti

### Struttura Dati Backup

```python
{
    "name": "Full backup 2026-02-15 17:16:00",
    "slug": "abc123def",
    "size": 275718144,  # bytes
    "size_mb": 263.01,  # MB
    "date": "2026-02-15",  # timezone locale
    "time": "17:16:00",   # timezone locale
    "datetime": datetime_object,  # timezone-aware
    "hash": "c1d68a4e...",  # SHA256
    "type": "full",
    "protected": False,
    "compressed": True,
    "destination": "local",  # codice
    "destination_name": "Home Assistant Locale"  # user-friendly
}
```

### Attributi Sensori

**sensor.backup_guardian_ultimo_backup**:
```yaml
backup_name: "Full backup 2026-02-15 17:16:00"
backup_date: "2026-02-15"
backup_time: "17:16:00"
backup_size: "263.01 MB"
backup_hash: "c1d68a4e227095fd..."
backup_type: "full"
backup_destination: "Home Assistant Locale"  # NUOVO v1.1.0
```

**sensor.backup_guardian_totale_backup**:
```yaml
backup_list:
  - name: "..."
    date: "..."
    time: "..."
    size: "... MB"
    hash: "..."
    destination: "Home Assistant Locale"  # NUOVO v1.1.0
```

---

## 🆕 Novità v1.1.0

### File Modificati

1. **`__init__.py`**: 
   - Aggiunta funzione `_copy_frontend_files()`
   - Copia automatica file JavaScript

2. **`const.py`**: 
   - Aggiunta `ATTR_BACKUP_DESTINATION`

3. **`coordinator.py`**: 
   - Fix conversione timezone UTC → locale
   - Parametro `source` in `_process_backup()`
   - Campi `destination` e `destination_name` nei dati

4. **`sensor.py`**: 
   - Attributo `backup_destination` in ultimo backup
   - Campo `destination` in lista backup

5. **`www/backup-guardian-card.js`**: 
   - CSS `.destination-badge`
   - Badge destinazione in UI
   - Visualizzazione destinazione per ogni backup

6. **Documentazione**: Tutti i file aggiornati

### File Aggiunti

- `icon.png` (PNG 256x256 con trasparenza)
- `logo.png` (PNG 256x256 con trasparenza)

---

## 🔜 Sviluppi Futuri

### File da Aggiungere

- `custom_components/backup_guardian/google_drive.py` - Google Drive integration
- `custom_components/backup_guardian/dropbox.py` - Dropbox integration
- `custom_components/backup_guardian/onedrive.py` - OneDrive integration
- `custom_components/backup_guardian/services.yaml` - Servizi custom

### Modifiche Pianificate

- Coordinator: Supporto multiple destinazioni
- Sensor: Sensori per ogni destinazione
- Card: Filtro per destinazione

---

## 📖 Per Sviluppatori

### Come Aggiungere una Nuova Destinazione

1. Aggiungi `destination` in `const.py`:
   ```python
   DESTINATIONS = ["local", "google_drive", "dropbox"]
   ```

2. Aggiorna `destination_map` in `coordinator.py`

3. Crea modulo destinazione (es. `google_drive.py`)

4. Aggiungi fetch backup dalla nuova destinazione in `_async_update_data()`

5. Testa e documenta

---

**Versione**: 1.1.0  
**Ultimo Aggiornamento**: 15 Febbraio 2026  
**Autore**: Leonardo (@leonardus1973)
