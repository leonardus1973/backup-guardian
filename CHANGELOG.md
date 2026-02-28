# Changelog

Tutte le modifiche importanti a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

---

## [1.2.0] - 2026-02-28

### ✨ Novità

#### 🌐 Integrazione Google Drive
- **Supporto Google Drive completo**: Backup Guardian ora monitora anche i backup su Google Drive!
- **OAuth2 sicuro**: Usa le tue credenziali Google personali (Client ID e Secret)
- **Merge automatico**: Visualizza backup locali e Google Drive insieme nella stessa card
- **Badge colorati per destinazione**:
  - 🏠 Celeste per Home Assistant Locale
  - 🟢 Verde per Google Drive
  - 🔴 Rosso per OneDrive (preparato per future integrazioni)
  - 🔵 Blu per Dropbox (preparato per future integrazioni)

#### ⚙️ Menu Configurazione
- **Config Flow rinnovato**: Menu opzioni per gestire Google Drive
- **Setup guidato OAuth2**: Flow passo-passo per autorizzazione Google
- **Folder ID configurabile**: Scegli quale cartella Drive monitorare

#### 🎨 Lovelace Card Migliorata
- **Badge colorati**: Ogni destinazione ha il suo colore ufficiale del brand
- **Bordi colorati**: Box backup con bordo sinistro colorato per destinazione
- **Scroll fisso**: Lista backup non torna più in alto automaticamente
- **Performance ottimizzate**: Aggiornamenti solo quando i dati cambiano realmente

### 🔧 Miglioramenti Tecnici
- Import Google API non bloccanti (uso di executor)
- Fix blocking call warnings
- Gestione corretta credenziali OAuth2
- Supporto pattern multipli backup (.tar, .tar.gz, .tgz)
- Contatori separati: `local_count` e `drive_count`

### 🐛 Bug Fix
- Risolto problema scroll automatico card Lovelace
- Fix error `'Credentials' object has no attribute 'request'`
- Fix `build() takes at most 2 positional arguments`
- Gestione corretta cache browser (Edge, iOS)

### 📦 Dipendenze
- Aggiunte: `google-api-python-client`, `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`

### 📚 Documentazione
- Aggiunta guida setup Google Cloud Console
- Documentazione OAuth2 flow completo
- Istruzioni configurazione Google Drive

---

## [1.1.0] - 2026-02-21

### ✨ Novità
- **Card Lovelace personalizzata**: Interfaccia grafica per visualizzare i backup
- **Lista espandibile**: Mostra tutti i backup con dettagli
- **Statistiche aggregate**: Totale backup e dimensione complessiva
- **Badge destinazione**: Indica dove è salvato ogni backup

### 🎨 Card Features
- Visualizzazione ultimo backup con tutti i dettagli
- Box statistiche (totale backup, MB totali)
- Lista espandibile/comprimibile
- Design responsive e moderno
- Icone e colori personalizzati

### 🔧 Miglioramenti
- Sensori più informativi
- Attributi estesi per ogni backup
- Hash MD5 per verifica integrità
- Timestamp precisi (data e ora separati)

---

## [1.0.0] - 2026-02-15

### 🎉 Release Iniziale

#### Funzionalità Base
- **Monitoraggio backup locale**: Legge i backup da Supervisor API
- **4 Sensori HA**:
  - `sensor.backup_guardian_totale_backup` - Contatore totale
  - `sensor.backup_guardian_dimensione_totale` - MB totali
  - `sensor.backup_guardian_ultimo_backup` - Nome ultimo backup
  - `sensor.backup_guardian_info_backup` - Dettagli ultimo backup

#### Attributi Backup
- Nome file
- Data e ora creazione
- Dimensione in MB
- Hash MD5
- Tipo (full/partial)
- Protezione password
- Slug identificativo

#### Automazioni
- Notifiche su nuovo backup
- Alert su spazio insufficiente
- Monitoraggio backup vecchi

### 🔒 Sicurezza
- Nessuna credential esterna richiesta
- Usa API Supervisor locale
- Permessi minimi necessari

### 📦 Installazione
- Supporto HACS
- Installazione manuale
- Configurazione via UI

---

## Legenda Emoji

- ✨ Novità
- 🔧 Miglioramenti
- 🐛 Bug Fix
- 🔒 Sicurezza
- 📚 Documentazione
- 🎨 UI/UX
- ⚙️ Configurazione
- 📦 Dipendenze
- 🌐 Integrazioni

---

## Link Utili

- [Repository GitHub](https://github.com/leonardus1973/backup-guardian)
- [Issues](https://github.com/leonardus1973/backup-guardian/issues)
- [Discussioni](https://github.com/leonardus1973/backup-guardian/discussions)
- [Donazioni PayPal](https://paypal.me/leonardopistoni)

---

**Grazie per usare Backup Guardian!** 🛡️
