# 📁 Struttura del Progetto - Backup Guardian

## Albero delle Directory

```
backup-guardian/
│
├── .github/                              # Configurazione GitHub
│   └── ISSUE_TEMPLATE/                   # Template per issue
│       ├── bug_report.md                 # Template segnalazione bug
│       └── feature_request.md            # Template richiesta funzionalità
│
├── custom_components/                    # Componenti custom per HA
│   └── backup_guardian/                  # Directory principale integrazione
│       │
│       ├── translations/                 # Traduzioni localizzate
│       │   └── it.json                   # Traduzione italiana
│       │
│       ├── www/                          # Risorse web (Lovelace card)
│       │   └── backup-guardian-card.js   # Card personalizzata JavaScript
│       │
│       ├── __init__.py                   # Inizializzazione integrazione
│       ├── config_flow.py                # Configurazione tramite UI
│       ├── const.py                      # Costanti e configurazioni
│       ├── coordinator.py                # Coordinatore aggiornamenti dati
│       ├── manifest.json                 # Metadati integrazione
│       ├── sensor.py                     # Definizione sensori
│       └── strings.json                  # Stringhe traduzioni base
│
├── .gitignore                            # File da ignorare in Git
├── CHANGELOG.md                          # Registro modifiche
├── CONTRIBUTING.md                       # Guida per collaboratori
├── ESEMPI_CONFIGURAZIONE.md              # Esempi configurazioni YAML
├── GUIDA_RAPIDA.md                       # Guida rapida installazione
├── LICENSE                               # Licenza MIT
├── README.md                             # Documentazione principale
├── STRUCTURE.md                          # Questo file
├── hacs.json                             # Configurazione HACS
└── info.md                               # Info per HACS
```

## Descrizione dei File

### 📂 `.github/`
Contiene configurazioni e template per GitHub.

#### `ISSUE_TEMPLATE/`
- **bug_report.md**: Template standardizzato per segnalare bug
- **feature_request.md**: Template per richiedere nuove funzionalità

### 📂 `custom_components/backup_guardian/`
Directory principale dell'integrazione Home Assistant.

#### File Python Core

**`__init__.py`**
- Punto di ingresso dell'integrazione
- Gestisce setup e teardown
- Inizializza il coordinator
- Setup delle piattaforme (sensori)

**`config_flow.py`**
- Gestisce la configurazione tramite UI
- Config flow per aggiungere l'integrazione
- Validazione configurazione

**`const.py`**
- Definisce tutte le costanti
- Percorsi dei backup
- Intervalli di aggiornamento
- Nomi attributi sensori

**`coordinator.py`**
- DataUpdateCoordinator per aggiornamento dati
- Scansione directory backup
- Calcolo hash SHA256
- Gestione informazioni backup

**`sensor.py`**
- Definizione dei 3 sensori principali:
  - Ultimo Backup
  - Totale Backup
  - Dimensione Totale Backup
- Gestione attributi sensori

#### File Configurazione

**`manifest.json`**
```json
{
  "domain": "backup_guardian",
  "name": "Backup Guardian",
  "version": "1.0.0",
  ...
}
```
Metadati dell'integrazione per Home Assistant.

**`strings.json`**
Stringhe di default per l'interfaccia utente.

**`translations/it.json`**
Traduzione italiana completa.

#### 📂 `www/`

**`backup-guardian-card.js`**
- Custom Lovelace card
- Interfaccia grafica interattiva
- Visualizzazione ultimo backup
- Lista espandibile di tutti i backup
- Design responsive e moderno

### 📄 File Root

**`README.md`**
- Documentazione completa del progetto
- Istruzioni installazione
- Guida configurazione
- Esempi d'uso
- Risoluzione problemi

**`GUIDA_RAPIDA.md`**
- Guida rapida in 3 passi
- Installazione veloce
- Configurazione essenziale
- FAQ principali

**`ESEMPI_CONFIGURAZIONE.md`**
- Esempi YAML completi
- Automazioni utili
- Script personalizzati
- Configurazioni dashboard

**`CHANGELOG.md`**
- Storico versioni
- Nuove funzionalità
- Bug fix
- Breaking changes

**`CONTRIBUTING.md`**
- Guida per contribuire
- Standard di codice
- Processo di review
- Codice di condotta

**`LICENSE`**
- Licenza MIT del progetto
- Termini d'uso
- Copyright

**`hacs.json`**
```json
{
  "name": "Backup Guardian",
  "content_in_root": false,
  "homeassistant": "2023.1.0"
}
```
Configurazione per HACS (Home Assistant Community Store).

**`info.md`**
- Breve descrizione per HACS
- Installazione quick start
- Link documentazione

**`.gitignore`**
- File da escludere da Git
- Cache Python
- File temporanei
- IDE settings

## 🔄 Flusso di Funzionamento

1. **Inizializzazione** (`__init__.py`)
   - Home Assistant carica l'integrazione
   - Viene creato il DataUpdateCoordinator
   - Si avvia la scansione dei backup

2. **Aggiornamento Dati** (`coordinator.py`)
   - Ogni 5 minuti scansiona `/backup`
   - Raccoglie info su ogni file .tar
   - Calcola hash SHA256
   - Aggiorna i sensori

3. **Sensori** (`sensor.py`)
   - Ricevono dati dal coordinator
   - Espongono state e attributi
   - Utilizzabili in automazioni e dashboard

4. **Lovelace Card** (`www/backup-guardian-card.js`)
   - Legge i dati dai sensori
   - Mostra ultimo backup
   - Lista espandibile tutti i backup
   - Interfaccia interattiva

## 📊 Dipendenze

### Home Assistant
- Versione minima: 2023.1.0
- Nessuna dipendenza esterna Python
- Usa solo librerie standard

### Frontend
- Vanilla JavaScript (no framework)
- Custom Elements API
- Home Assistant Lovelace API

## 🎯 Punti di Estensione

### Aggiungere Nuove Piattaforme di Backup

1. Modificare `coordinator.py`:
   - Aggiungere metodi per la nuova piattaforma
   - Implementare scan e verifica

2. Modificare `const.py`:
   - Aggiungere costanti specifiche

3. Aggiornare `sensor.py`:
   - Aggiungere attributi se necessari

### Aggiungere Nuovi Sensori

1. Creare classe in `sensor.py`:
```python
class NuovoSensor(CoordinatorEntity, SensorEntity):
    # Implementazione
```

2. Registrare in `async_setup_entry`:
```python
sensors.append(NuovoSensor(coordinator, entry))
```

### Modificare la Card

Editare `www/backup-guardian-card.js`:
- Aggiungere nuove sezioni HTML
- Modificare stili CSS
- Aggiungere interazioni JavaScript

## 🔐 Sicurezza

- **Hash SHA256**: Verifica integrità backup
- **Read-only**: Solo lettura directory backup
- **No credenziali**: Nessuna password memorizzata
- **Local-first**: Tutto locale, nessun cloud

## 📱 Compatibilità

- ✅ Home Assistant OS
- ✅ Home Assistant Container
- ✅ Home Assistant Core
- ✅ Home Assistant Supervised

## 🚀 Performance

- **Memoria**: ~5-10MB
- **CPU**: Minimo impatto
- **Disco**: Solo lettura, nessuna scrittura
- **Network**: Nessun traffico (solo locale)

## 📈 Metriche

- **Linee di codice Python**: ~300
- **Linee di codice JavaScript**: ~200
- **File documentazione**: 8
- **Lingue supportate**: Italiano (estendibile)

---

**Versione documento**: 1.0.0  
**Data ultimo aggiornamento**: 31 Gennaio 2026
