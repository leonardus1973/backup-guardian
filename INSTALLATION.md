# 📦 Guida Installazione Completa - Backup Guardian v1.1.0

Questa guida ti accompagna passo-passo nell'installazione di Backup Guardian.

## 📋 Prerequisiti

Prima di iniziare, verifica di avere:

- ✅ **Home Assistant OS** 2023.1.0 o superiore
- ✅ Oppure **Home Assistant Supervised** 2023.1.0 o superiore
- ✅ Accesso come amministratore
- ✅ Almeno un backup presente nel sistema

⚠️ **Non compatibile** con:
- ❌ Home Assistant Container (Docker standalone)
- ❌ Home Assistant Core (installazione Python)

---

## 🎯 Metodo 1: Installazione via HACS (Consigliato)

### Passo 1: Aggiungi Repository Personalizzato

1. Apri **HACS** nel menu laterale di Home Assistant
2. Clicca su **Integrazioni**
3. Clicca sui **tre puntini** in alto a destra
4. Seleziona **Repository personalizzati**
5. Nella finestra che si apre:
   - **Repository**: `https://github.com/leonardus1973/backup-guardian`
   - **Categoria**: `Integration`
6. Clicca **Aggiungi**

### Passo 2: Installa l'Integrazione

1. Nella sezione **Integrazioni** di HACS
2. Cerca "**Backup Guardian**"
3. Clicca sulla card dell'integrazione
4. Clicca **Scarica** (o **Download**)
5. Nella finestra di conferma, clicca **Scarica**
6. Aspetta il completamento del download

### Passo 3: Riavvia Home Assistant

1. Vai su **Impostazioni** → **Sistema** → **Riavvia**
2. Clicca **Riavvia**
3. Aspetta che Home Assistant si riavvii completamente (~2 minuti)

✅ **Durante il riavvio, l'integrazione copia automaticamente il file JavaScript della card in `/config/www/community/backup_guardian/`!**

### Passo 4: Configura l'Integrazione

1. Vai su **Impostazioni** → **Dispositivi e Servizi**
2. Clicca **+ Aggiungi Integrazione**
3. Nella barra di ricerca, digita "**Backup Guardian**"
4. Clicca sull'integrazione quando appare
5. Nella finestra di configurazione, clicca **Invia**
6. Vedrai il messaggio "Integrazione aggiunta con successo"

✅ **I 3 sensori vengono creati automaticamente!**

### Passo 5: Verifica i Sensori

1. Vai su **Strumenti per sviluppatori** → **Stati**
2. Nella barra di ricerca, digita `backup_guardian`
3. Dovresti vedere 3 sensori:
   - `sensor.backup_guardian_ultimo_backup`
   - `sensor.backup_guardian_totale_backup`
   - `sensor.backup_guardian_dimensione_totale`
4. Clicca su `sensor.backup_guardian_ultimo_backup`
5. Verifica che abbia valori e attributi corretti

---

## 🎨 Metodo 2: Installazione Manuale

### Passo 1: Scarica i File

1. Vai su https://github.com/leonardus1973/backup-guardian/releases
2. Scarica l'ultima versione (v1.1.0 o superiore)
3. Clicca su `Source code (zip)`

### Passo 2: Estrai e Copia i File

1. Estrai il file ZIP scaricato
2. All'interno troverai la cartella `custom_components/backup_guardian`
3. Copia l'intera cartella `backup_guardian` in `/config/custom_components/`
4. La struttura finale deve essere:
   ```
   /config/custom_components/backup_guardian/
   ├── __init__.py
   ├── config_flow.py
   ├── const.py
   ├── coordinator.py
   ├── manifest.json
   ├── sensor.py
   ├── strings.json
   ├── translations/
   │   └── it.json
   └── www/
       └── backup-guardian-card.js
   ```

### Passo 3: Riavvia Home Assistant

Segui il **Passo 3** del Metodo 1 (riavvio).

✅ **Durante il riavvio, l'integrazione copia automaticamente il file JavaScript!**

### Passo 4-5: Configura e Verifica

Segui i **Passi 4 e 5** del Metodo 1.

---

## 🎨 Configurazione Lovelace Card

### Passo 1: Verifica File JavaScript

Prima di procedere, verifica che il file sia stato copiato:

1. Con **File Editor** o **SSH**, controlla che esista:
   ```
   /config/www/community/backup_guardian/backup-guardian-card.js
   ```

Se **non esiste**:
- Riavvia Home Assistant di nuovo
- L'integrazione lo copia automaticamente al primo avvio

### Passo 2: Registra la Risorsa

1. Vai su **Impostazioni** → **Dashboard** → **Risorse**
2. Clicca **+ Aggiungi risorsa**
3. Compila i campi:
   - **URL**: `/local/community/backup_guardian/backup-guardian-card.js`
   - **Tipo di risorsa**: **Modulo JavaScript**
4. Clicca **Crea**

### Passo 3: Svuota Cache Browser

**⚠️ MOLTO IMPORTANTE!**

La cache del browser può impedire il caricamento della card.

**Windows/Linux:**
- Ctrl + Shift + R (hard refresh)
- Oppure Ctrl + F5

**Mac:**
- Cmd + Shift + R

**Se ancora non funziona:**
1. Vai su `edge://settings/clearBrowserData` (o equivalente per il tuo browser)
2. Seleziona **"Immagini e file memorizzati nella cache"**
3. Clicca **Cancella dati**
4. **Chiudi completamente il browser**
5. Riapri il browser

### Passo 4: Aggiungi la Card alla Dashboard

1. Apri una dashboard
2. Clicca sui **tre puntini** in alto a destra
3. Seleziona **Modifica dashboard**
4. Clicca **+ Aggiungi Card**
5. Scorri in basso e seleziona **Manuale**
6. Incolla questa configurazione:

```yaml
type: custom:backup-guardian-card
entity: sensor.backup_guardian_totale_backup
last_backup_entity: sensor.backup_guardian_ultimo_backup
size_entity: sensor.backup_guardian_dimensione_totale
```

7. Clicca **Salva**
8. Clicca **Fine** per uscire dalla modalità modifica

### Passo 5: Verifica la Card

Dovresti vedere:

- ✅ Header "🛡️ Backup Guardian"
- ✅ Sezione "📦 Ultimo Backup" con badge **[HOME ASSISTANT LOCALE]**
- ✅ Due box statistiche con numero backup e MB totali
- ✅ Bottone "Mostra Tutti i Backup"
- ✅ Lista espandibile con badge per ogni backup

Se **non vedi** la card:
1. Apri **Console** del browser (F12)
2. Cerca il messaggio `✅ Backup Guardian Card loaded successfully!`
3. Se non c'è, il file non si sta caricando → Svuota di nuovo la cache

---

## ✅ Verifica Installazione Completa

### Checklist Finale

- [ ] Integrazione presente in **Dispositivi e Servizi**
- [ ] 3 sensori attivi con valori corretti
- [ ] File JavaScript esiste in `/config/www/community/backup_guardian/`
- [ ] Risorsa registrata in **Dashboard** → **Risorse**
- [ ] Cache browser svuotata
- [ ] Card visibile nella dashboard
- [ ] Badge destinazione visibili
- [ ] Orari corretti (timezone locale)
- [ ] Console mostra messaggio di caricamento card

Se tutti i punti sono ✅, l'installazione è **completata con successo**! 🎉

---

## 🐛 Risoluzione Problemi Comuni

### Problema: Sensori non creati o vuoti

**Soluzione:**
1. Verifica di essere su **HA OS** o **Supervised**
2. Controlla log: **Impostazioni** → **Sistema** → **Log**
3. Cerca errori con `backup_guardian`
4. Se vedi errori di permessi, verifica che ci sia almeno un backup nel sistema
5. Riavvia l'integrazione: **Dispositivi e Servizi** → Backup Guardian → **Tre puntini** → **Ricarica**

### Problema: File JavaScript non copiato

**Soluzione:**
1. Verifica log per messaggi di copia file
2. Se vedi errori, copia manualmente:
   - Da: `/config/custom_components/backup_guardian/www/backup-guardian-card.js`
   - A: `/config/www/community/backup_guardian/backup-guardian-card.js`
3. Crea la directory se non esiste
4. Riavvia Home Assistant

### Problema: Card mostra "Custom element doesn't exist"

**Soluzione:**
1. Verifica che il file esista in `/config/www/community/backup_guardian/backup-guardian-card.js`
2. Verifica che l'URL risorsa sia esatto: `/local/community/backup_guardian/backup-guardian-card.js`
3. **Svuota cache browser completamente** (vedi Passo 3 sopra)
4. Prova in **modalità incognito** per escludere problemi di cache
5. Riavvia Home Assistant

### Problema: Badge destinazione non appaiono

**Soluzione:**
1. Verifica versione: deve essere **v1.1.0** o superiore
2. Svuota cache browser completamente
3. Verifica attributo nei sensori:
   - **Strumenti per sviluppatori** → **Stati**
   - `sensor.backup_guardian_ultimo_backup`
   - Deve esserci `backup_destination: Home Assistant Locale`
4. Se manca l'attributo, reinstalla l'integrazione

### Problema: Orari sbagliati (-1 ora)

**Soluzione:**
Questo bug è stato risolto nella v1.1.0. Se hai ancora il problema:
1. Aggiorna alla v1.1.0 o superiore
2. Verifica timezone HA: **Impostazioni** → **Sistema** → **Generale**
3. Ricarica integrazione

---

## 📝 Abilitare Log di Debug

Se hai problemi persistenti, abilita i log dettagliati:

1. Modifica `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.backup_guardian: debug
```

2. Riavvia Home Assistant
3. Vai su **Impostazioni** → **Sistema** → **Log**
4. Cerca messaggi di `backup_guardian`
5. Riporta gli errori aprendo un [Issue su GitHub](https://github.com/leonardus1973/backup-guardian/issues)

---

## 🎓 Passi Successivi

Dopo l'installazione:

1. 📖 Leggi il [README](https://github.com/leonardus1973/backup-guardian) per funzionalità avanzate
2. 🤖 Configura [automazioni](ESEMPI_CONFIGURAZIONE.md) per notifiche backup
3. ⭐ Lascia una stella su GitHub se il progetto ti è utile
4. 🐛 Segnala bug o suggerisci funzionalità tramite [Issues](https://github.com/leonardus1973/backup-guardian/issues)

---

**Installazione completata! Buon monitoraggio! 🛡️**

**Backup Guardian v1.1.0** - Prima versione stabile e completa
