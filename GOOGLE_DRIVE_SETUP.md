# 🔐 Google Drive Integration - Setup Guide

Questa guida ti aiuta a configurare l'integrazione Google Drive per Backup Guardian.

## 📋 Prerequisiti

- Account Google
- Backup già caricati su Google Drive (in una cartella specifica)
- 15 minuti di tempo

---

## 🚀 FASE 1: Crea Progetto Google Cloud

### Step 1: Accedi a Google Cloud Console

1. Vai su https://console.cloud.google.com
2. **Accedi** con il tuo account Google
3. Se è la prima volta, accetta i Termini di Servizio

### Step 2: Crea Nuovo Progetto

1. Clicca sul **menu a tendina** del progetto (in alto)
2. Clicca **"Nuovo Progetto"**
3. **Nome progetto**: `Home Assistant Backup Guardian`
4. **Organizzazione**: Lascia come predefinito
5. Clicca **"Crea"**
6. Aspetta che il progetto venga creato (~30 secondi)
7. **Seleziona** il nuovo progetto dal menu

---

## 🔌 FASE 2: Abilita Google Drive API

### Step 3: Abilita API

1. Nel menu laterale, vai su **"API e servizi"** → **"Libreria"**
2. Nella barra di ricerca, digita: `Google Drive API`
3. Clicca su **"Google Drive API"**
4. Clicca **"Abilita"**
5. Aspetta l'attivazione (~10 secondi)

---

## 🔑 FASE 3: Crea Credenziali OAuth 2.0

### Step 4: Configura Schermata Consenso OAuth

1. Nel menu laterale, vai su **"API e servizi"** → **"Schermata consenso OAuth"**
2. Seleziona **"Esterno"** (External)
3. Clicca **"Crea"**

**Pagina 1 - Informazioni App**:
- **Nome applicazione**: `Backup Guardian`
- **Email assistenza utente**: La tua email
- **Logo applicazione**: (Opzionale - puoi saltare)
- **Dominio app**: (Lascia vuoto)
- **Link informativa privacy**: (Lascia vuoto per uso personale)
- **Link termini di servizio**: (Lascia vuoto)
- **Email sviluppatore**: La tua email
- Clicca **"Salva e continua"**

**Pagina 2 - Ambiti (Scopes)**:
- Clicca **"Aggiungi o rimuovi ambiti"**
- Cerca e seleziona: `.../auth/drive.readonly` (Google Drive - Solo lettura)
- Clicca **"Aggiorna"**
- Clicca **"Salva e continua"**

**Pagina 3 - Utenti test**:
- Clicca **"+ Aggiungi utenti"**
- Inserisci la **tua email**
- Clicca **"Aggiungi"**
- Clicca **"Salva e continua"**

**Pagina 4 - Riepilogo**:
- Controlla i dati
- Clicca **"Torna alla dashboard"**

### Step 5: Crea Credenziali

1. Nel menu laterale, vai su **"API e servizi"** → **"Credenziali"**
2. Clicca **"+ Crea credenziali"** in alto
3. Seleziona **"ID client OAuth"**

**Configura Credenziali**:
- **Tipo applicazione**: `App desktop` (Desktop app)
- **Nome**: `Home Assistant Backup Guardian`
- Clicca **"Crea"**

### Step 6: Salva le Credenziali

Apparirà una finestra con:
- **ID client**: `123456789.apps.googleusercontent.com`
- **Segreto client**: `abcdef-xyz123`

⚠️ **IMPORTANTE**: 
- **Copia** entrambi i valori
- **Salva** in un posto sicuro (ti serviranno in Home Assistant)
- Clicca **"OK"**

---

## 📁 FASE 4: Prepara Cartella Drive

### Step 7: Identifica Cartella Backup

1. Vai su https://drive.google.com
2. Naviga alla **cartella** dove hai i backup
3. **Apri** la cartella
4. Guarda l'**URL** nella barra degli indirizzi:
   ```
   https://drive.google.com/drive/folders/CARTELLA_ID_QUI
   ```
5. **Copia** il `CARTELLA_ID_QUI` (stringa alfanumerica)

**Esempio**:
```
URL: https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRsTuVwXyZ
Folder ID: 1aBcDeFgHiJkLmNoPqRsTuVwXyZ
```

**Alternativa**: Puoi anche usare la cartella **root** di Drive:
- Folder ID: `root`

---

## 🏠 FASE 5: Configura in Home Assistant

### Step 8: Aggiungi Google Drive a Backup Guardian

1. In Home Assistant, vai su **Impostazioni** → **Dispositivi e Servizi**
2. Trova **"Backup Guardian"**
3. Clicca **"Configura"** (o **"Opzioni"**)
4. Seleziona **"Abilita Google Drive"**

**Inserisci i Dati**:
- **Client ID**: Incolla l'ID client copiato prima
- **Client Secret**: Incolla il segreto client
- **Folder ID**: Incolla l'ID cartella Drive (o `root`)
- Clicca **"Avanti"**

### Step 9: Autorizza Accesso

1. Si aprirà un **link di autorizzazione Google**
2. **Clicca** sul link (o copialo nel browser)
3. **Accedi** con il tuo account Google
4. Google mostrerà: *"Backup Guardian vuole accedere a Google Drive"*
5. Clicca **"Consenti"** (Allow)
6. Google mostrerà un **codice** (es. `4/0AfJoh...`)
7. **Copia** il codice completo
8. **Incolla** il codice in Home Assistant
9. Clicca **"Autorizza"**

✅ **Fatto!** L'integrazione ora ha accesso ai tuoi backup su Drive!

---

## ✅ Verifica Funzionamento

### Step 10: Controlla i Sensori

1. Vai su **Strumenti per sviluppatori** → **Stati**
2. Cerca `sensor.backup_guardian_ultimo_backup`
3. Negli **attributi**, dovresti vedere backup con:
   - `destination: "Google Drive"`

### Step 11: Controlla la Card

Nella card Lovelace, dovresti vedere:
- Badge **[GOOGLE DRIVE]** sui backup da Drive
- Badge **[HOME ASSISTANT LOCALE]** sui backup locali
- Totale unificato

---

## 🐛 Risoluzione Problemi

### Errore: "Client ID non valido"
**Soluzione**: 
- Controlla di aver copiato tutto l'ID client
- Deve finire con `.apps.googleusercontent.com`

### Errore: "Accesso negato"
**Soluzione**: 
- Verifica di aver abilitato Google Drive API
- Controlla di essere nell'elenco "Utenti test"

### Errore: "Nessun backup trovato"
**Soluzione**: 
- Verifica che i file siano `.tar` o `.tar.gz`
- Controlla che il Folder ID sia corretto
- Prova a usare `root` come Folder ID

### Errore: "Token scaduto"
**Soluzione**: 
- Vai in **Dispositivi e Servizi** → Backup Guardian → **"Riautorizza"**
- Ripeti il flusso OAuth

---

## 🔒 Sicurezza e Privacy

### Cosa Può Fare Backup Guardian?
- ✅ **Leggere** i file nella cartella specificata
- ✅ **Vedere** metadati (nome, dimensione, data)
- ❌ **NON può** modificare, eliminare o creare file
- ❌ **NON può** accedere ad altre cartelle

### Dove Sono Salvate le Credenziali?
- **Localmente** nel database di Home Assistant
- **Criptate** con chiave segreta HA
- **Mai inviate** a server esterni

### Posso Revocare l'Accesso?
Sì, in qualsiasi momento:
1. Vai su https://myaccount.google.com/permissions
2. Trova "Backup Guardian"
3. Clicca **"Rimuovi accesso"**

---

## 💡 Consigli

### Organizzazione Cartelle
Consigliata:
```
Google Drive/
└── Backups/
    └── HomeAssistant/
        ├── backup_2026-02-15.tar
        ├── backup_2026-02-14.tar
        └── ...
```

Usa l'ID della cartella `HomeAssistant/`!

### Sincronizzazione Automatica
Per caricare backup automaticamente su Drive, usa addon come:
- **sabeechen/hassio-google-drive-backup** (consigliato)
- **Dropbox Backup** (alternativa)

Backup Guardian li **legge** automaticamente!

---

## 📞 Supporto

Problemi? 
- [Apri Issue su GitHub](https://github.com/leonardus1973/backup-guardian/issues)
- Includi i log: `custom_components.backup_guardian: debug`

---

**Setup completato! Buon backup! 🛡️☁️**
