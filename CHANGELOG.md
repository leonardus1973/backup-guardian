# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.0] - 2026-01-31

### Aggiunto
- ✨ Prima release pubblica di Backup Guardian
- 📊 Monitoraggio completo dei backup locali di Home Assistant
- 🔍 Verifica hash SHA256 per ogni backup
- 📈 Tre sensori principali:
  - `sensor.ultimo_backup` - Informazioni sull'ultimo backup
  - `sensor.totale_backup` - Numero totale di backup
  - `sensor.dimensione_totale_backup` - Spazio totale occupato
- 🎨 Lovelace card personalizzata con interfaccia intuitiva
- 🔄 Aggiornamento automatico ogni 5 minuti
- 📝 Documentazione completa in italiano
- 🌐 Supporto per HACS
- 🎯 Config flow per configurazione tramite UI
- 🌍 Traduzioni italiane complete

### Caratteristiche della Card
- Visualizzazione dettagliata ultimo backup
- Bottone espandibile per lista completa backup
- Design moderno e responsive
- Integrazione nativa con tema di Home Assistant

### Documentazione
- README completo con istruzioni dettagliate
- Guida rapida per installazione veloce
- Esempi di configurazione e automazioni
- File info.md per HACS

## [Unreleased]

### Pianificato per versioni future
- 🌐 Supporto Google Drive
- 📦 Supporto Dropbox
- 🔔 Notifiche push personalizzate
- 🤖 Automazioni integrate per pulizia backup
- 📊 Grafici storici dei backup
- 🔐 Backup differenziali
- ⚙️ Opzioni di configurazione avanzate
- 🌍 Traduzioni in altre lingue
- 📱 Supporto app mobile nativa

---

## Legenda

- `Aggiunto` - Nuove funzionalità
- `Modificato` - Cambiamenti a funzionalità esistenti
- `Deprecato` - Funzionalità che verranno rimosse
- `Rimosso` - Funzionalità rimosse
- `Corretto` - Bug fix
- `Sicurezza` - Vulnerabilità corrette
