# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.1.0] - 2026-02-15

### 🎉 Prima Release Completamente Funzionante!

Questa è la **prima versione stabile e completa** di Backup Guardian, pronta per l'uso in produzione!

### Added
- ✨ **Campo Destinazione Backup**: Ogni backup ora mostra la sua destinazione (Home Assistant Locale, Google Drive, ecc.)
- 🎨 **Badge Colorati nella Card**: Interfaccia rinnovata con badge che indicano visivamente la destinazione
- 🔄 **Copia Automatica File Frontend**: Il file JavaScript della card viene copiato automaticamente in `/www/community/`
- 📍 **Struttura Multi-Destinazione**: Codice preparato per future integrazioni cloud (Google Drive, Dropbox, OneDrive)
- 📝 **Attributo `backup_destination`**: Nuovo attributo nei sensori per identificare la destinazione

### Fixed
- 🕐 **Fix Timezone Critico**: Gli orari ora sono corretti (risolto problema -1 ora)
- 🐛 **Conversione Data UTC → Locale**: Uso corretto di `dt_util` per fuso orario
- 🔧 **Import Python 3.13**: Rimosso `zoneinfo`, uso solo moduli HA nativi
- 📦 **Copia Automatica Card**: Non serve più copiare manualmente il file JavaScript
- 🏷️ **Versione Dispositivo**: Auto-read da `manifest.json`

### Changed
- 🎨 **UI Card Rinnovata**: Design moderno con badge destinazione
- 📊 **Visualizzazione Migliorata**: Layout più chiaro e intuitivo
- 🔄 **Gestione Robusta Date**: Parsing date con fallback multipli
- 📝 **Documentazione Completa**: README e guide aggiornate

---

## [1.0.18] - 2026-02-15

### Fixed
- 🔧 **Auto-copy Frontend Files**: Implementato sistema automatico di copia file JavaScript
- 📁 **Directory Creation**: Creazione automatica `/www/community/backup_guardian/`
- 🔄 **File Update Detection**: Aggiornamento automatico file quando cambia versione

---

## [1.0.17] - 2026-02-14

### Fixed
- 🐛 **Fix Timezone Conversion**: Risolto problema conversione orari UTC → locale
- 🕐 **Orari Corretti**: Non più differenza di 1 ora tra orario backup e visualizzazione

---

## [1.0.13] - 2026-02-14

### Added
- 📍 **Preparazione Multi-Destinazione**: Aggiunta struttura per supporto future destinazioni
- 🏷️ **Attributo Destinazione**: Preparazione campo `destination` nei dati backup

---

## [1.0.12] - 2026-02-01

### Fixed
- 🎨 **Icone PNG**: Aggiunte icone con trasparenza corretta
- 🖼️ **Logo Display**: Fix visualizzazione icone nel browser

---

## [1.0.11] - 2026-02-01

### Added
- 📚 **Documentazione Estesa**: README completo con troubleshooting
- 🔧 **Sezione Debug**: Istruzioni per abilitare log dettagliati
- 📝 **Esempi Automazioni**: Notifiche backup mancante e nuovo backup

### Changed
- 📖 **README Riscritto**: Struttura migliorata e più chiara
- 🔄 **Istruzioni Cache**: Focus su problemi cache browser

---

## [1.0.9] - 2026-01-31

### Fixed
- 🔧 **Supervisor API Access**: Uso corretto `hassio_component.send_command()`
- 📏 **Dimensioni Backup Corrette**: Risolto problema 0 MB
- 🏷️ **Versione Dispositivo**: Auto-read da manifest.json
- 🎨 **Lovelace Card Fix**: Rimosso dipendenze `ha-icon`

### Changed
- 🔄 **Coordinator Aggiornato**: Migliore gestione API Supervisor
- 📦 **Sensor.py Ottimizzato**: Lettura versione automatica
- 🎨 **Card UI**: Uso emoji invece di componenti HA

---

## [1.0.7] - 2026-01-31

### Added
- ✨ **Prima Versione Funzionante**: Integrazione operativa
- 📊 **Supervisor API Integration**: Connessione stabile
- 🎨 **Lovelace Card**: Card personalizzata
- 📈 **3 Sensori Attivi**: Dati corretti e aggiornati

### Fixed
- 🔧 **API Access**: Fix accesso Supervisor per HA OS
- 📏 **Calcolo Dimensioni**: Fix conversione bytes → MB

---

## [1.0.0] - 2026-01-31

### Added - Prima Release Pubblica
- ✨ **Lancio Iniziale** di Backup Guardian
- 📊 **Monitoraggio Backup**: Backup locali Home Assistant
- 🔍 **Hash SHA256**: Verifica integrità per ogni backup
- 📈 **3 Sensori Principali**:
  - `sensor.ultimo_backup` - Informazioni ultimo backup
  - `sensor.totale_backup` - Numero totale backup
  - `sensor.dimensione_totale_backup` - Spazio occupato
- 🎨 **Lovelace Card Personalizzata**: Interfaccia intuitiva
- 🔄 **Aggiornamento Automatico**: Ogni 5 minuti
- 📝 **Documentazione Italiana**: Completa
- 🌐 **Supporto HACS**: Installazione facilitata
- 🎯 **Config Flow UI**: Configurazione tramite interfaccia
- 🌍 **Traduzioni**: Interfaccia in italiano

### Caratteristiche Card
- Visualizzazione ultimo backup dettagliata
- Bottone espandibile per lista completa
- Design responsive integrato con tema HA
- Informazioni hash SHA256 per ogni backup

---

## [Unreleased]

### Pianificato per Versioni Future
- 🌐 **Google Drive Integration**: Backup automatici su Google Drive
- 📦 **Dropbox Support**: Sincronizzazione con Dropbox
- ☁️ **OneDrive Support**: Backup su Microsoft OneDrive
- 🔔 **Notifiche Push Avanzate**: Sistema notifiche personalizzato
- 🤖 **Automazioni Intelligenti**: Pulizia automatica backup vecchi
- 📊 **Grafici Storici**: Visualizzazione trend backup
- 🔐 **Backup Differenziali**: Ottimizzazione spazio
- ⚙️ **Configurazione Avanzata**: Opzioni personalizzazione
- 🌍 **Multi-lingua**: Traduzioni in altre lingue
- 📱 **App Mobile Nativa**: Gestione da smartphone
- ✅ **Verifica Integrità Automatica**: Test backup programmati
- 📄 **Export CSV**: Esportazione lista backup
- 🔄 **Restore Automatico**: Ripristino facilitato
- 📈 **Analytics**: Statistiche utilizzo storage

---

## Legenda Emoji

- ✨ `Added` - Nuove funzionalità
- 🔧 `Changed` - Modifiche a funzionalità esistenti
- 🗑️ `Deprecated` - Funzionalità che verranno rimosse
- ❌ `Removed` - Funzionalità rimosse
- 🐛 `Fixed` - Bug fix
- 🔒 `Security` - Vulnerabilità corrette
- 📝 `Documentation` - Aggiornamenti documentazione
- 🎨 `UI/UX` - Miglioramenti interfaccia
- 📊 `Data` - Modifiche gestione dati
- 🔄 `Refactoring` - Ristrutturazione codice

---

**Note sulla Versione 1.1.0:**

Questa è la prima versione **completamente stabile e testata** di Backup Guardian. Tutte le funzionalità core sono operative e testate:

- ✅ Monitoraggio backup locale funzionante
- ✅ Dimensioni e orari corretti
- ✅ Card Lovelace con auto-installazione
- ✅ Badge destinazione visualizzati
- ✅ Compatibilità Python 3.13
- ✅ Zero configurazione manuale richiesta

**Consigliato per uso in produzione!** 🎉
