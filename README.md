# 🛡️ Backup Guardian

[![Version](https://img.shields.io/github/v/release/leonardus1973/backup-guardian)](https://github.com/leonardus1973/backup-guardian/releases)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.1+-blue)](https://www.home-assistant.io)
[![License](https://img.shields.io/github/license/leonardus1973/backup-guardian)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)


**Monitora i tuoi backup di Home Assistant con stile!** 🚀

Integrazione personalizzata per Home Assistant che tiene traccia di tutti i tuoi backup, sia locali che su cloud: Google Drive (Dropbox, OneDrive, NAS - in arrivo).

---

## ✨ Novità v1.2.0: Google Drive Integration!

🌟 **Ora con supporto Google Drive!** 🌟

- ☁️ Monitora backup su Google Drive
- 🔄 Merge automatico backup locali + cloud
- 🎨 Badge colorati per ogni destinazione
- 🔐 OAuth2 sicuro con le tue credenziali

---

## 📸 Screenshot

### Card Lovelace con Google Drive
![Backup Guardian Card](docs/images/card-screenshot.png)

### Configurazione Google Drive
![Google Drive Setup](docs/images/google-drive-setup.png)

---

## 🎯 Funzionalità

### 📦 Monitoraggio Multi-Destinazione
- ✅ **Home Assistant Locale** - Backup nel NAS/storage locale
- ✅ **Google Drive** - Backup sincronizzati su cloud
- 🔜 **Dropbox** - In arrivo
- 🔜 **OneDrive** - In arrivo

### 🎨 Card Lovelace Personalizzata
- **Badge colorati per destinazione**:
  - 🏠 Celeste per Home Assistant Locale
  - 🟢 Verde per Google Drive
  - 🔴 Rosso per OneDrive
  - 🔵 Blu per Dropbox
- **Ultimo backup** con tutti i dettagli
- **Statistiche aggregate** (totale backup, MB totali)
- **Lista espandibile** di tutti i backup
- **Design moderno** e responsive

### 📊 4 Sensori Informativi
- `sensor.backup_guardian_totale_backup` - Numero totale backup
- `sensor.backup_guardian_dimensione_totale` - MB totali
- `sensor.backup_guardian_ultimo_backup` - Nome ultimo backup
- `sensor.backup_guardian_info_backup` - Dettagli completi

### 🔔 Automazioni Pronte
- Notifiche su nuovo backup
- Alert su backup vecchi
- Monitoraggio spazio disponibile

---

## 📥 Installazione

### Via HACS (Consigliato)

1. Apri **HACS** nel tuo Home Assistant
2. Vai su **Integrazioni**
3. Clicca **⋮** (menu) → **Repository personalizzati**
4. Aggiungi: `https://github.com/leonardus1973/backup-guardian`
5. Categoria: **Integrazione**
6. Clicca **"Backup Guardian"** → **Scarica**
7. **Riavvia Home Assistant**
8. Vai su **Impostazioni** → **Dispositivi e Servizi** → **Aggiungi Integrazione**
9. Cerca **"Backup Guardian"** e aggiungila

### Manuale

1. Scarica la [ultima release](https://github.com/leonardus1973/backup-guardian/releases)
2. Copia la cartella `custom_components/backup_guardian` in `/config/custom_components/`
3. Riavvia Home Assistant
4. Aggiungi l'integrazione dalla UI

---

## ⚙️ Configurazione

### 1. Aggiungi l'Integrazione

**Impostazioni** → **Dispositivi e Servizi** → **Aggiungi Integrazione** → Cerca **"Backup Guardian"**

### 2. Configura Google Drive (Opzionale)

#### Prerequisiti: Setup Google Cloud Console

Prima di configurare Google Drive in Home Assistant, devi creare le credenziali OAuth2:

1. **Vai su** [Google Cloud Console](https://console.cloud.google.com)
2. **Crea un nuovo progetto** o selezionane uno esistente
3. **Abilita Google Drive API**:
   - Menu → API e servizi → Libreria
   - Cerca "Google Drive API" → Abilita
4. **Configura schermata consenso OAuth**:
   - Menu → API e servizi → Schermata consenso OAuth
   - Tipo: **Esterno**
   - Nome app: `Backup Guardian`
   - Email assistenza: la tua email
   - Aggiungi ambito: `https://www.googleapis.com/auth/drive.readonly`
   - Utenti test: aggiungi la tua email Google
5. **Crea credenziali OAuth 2.0**:
   - Menu → Credenziali → + Crea credenziali
   - Tipo: **ID client OAuth** → **App desktop**
   - Nome: `Backup Guardian`
   - Salva **Client ID** e **Client Secret**

#### Configurazione in Home Assistant

1. **Dispositivi e Servizi** → **Backup Guardian** → **Configura**
2. Clicca **"Integrazione Google Drive"**
3. **Abilita Google Drive** ✅
4. Inserisci:
   - **Client ID** (dalla Google Cloud Console)
   - **Client Secret** (dalla Google Cloud Console)
   - **Folder ID** (vedi sotto)
5. Clicca sul **link di autorizzazione Google**
6. Accedi con il tuo account Google
7. Autorizza l'app
8. Copia il **codice di autorizzazione**
9. Incolla in Home Assistant → **Invia**

#### Come Trovare il Folder ID

**Metodo 1: Dall'URL**
1. Vai su [Google Drive](https://drive.google.com)
2. Apri la cartella con i backup
3. Guarda l'URL: `https://drive.google.com/drive/folders/FOLDER_ID_QUI`
4. Copia solo `FOLDER_ID_QUI`

**Metodo 2: Root**
- Inserisci `root` per monitorare la cartella principale

---

## 🎨 Card Lovelace

### Installazione Card

La card viene installata automaticamente con l'integrazione!

### Configurazione Card

Aggiungi alla tua dashboard:

```yaml
type: custom:backup-guardian-card
entity: sensor.backup_guardian_totale_backup
last_backup_entity: sensor.backup_guardian_ultimo_backup
size_entity: sensor.backup_guardian_dimensione_totale
```

### Opzioni Card

| Opzione | Tipo | Richiesto | Default | Descrizione |
|---------|------|-----------|---------|-------------|
| `entity` | string | Sì | - | Sensore totale backup |
| `last_backup_entity` | string | No | `sensor.backup_guardian_ultimo_backup` | Sensore ultimo backup |
| `size_entity` | string | No | `sensor.backup_guardian_dimensione_totale` | Sensore dimensione |

---

## 🔔 Esempi Automazioni

### Notifica Nuovo Backup

```yaml
automation:
  - alias: "Notifica Nuovo Backup"
    trigger:
      - platform: state
        entity_id: sensor.backup_guardian_ultimo_backup
    action:
      - service: notify.mobile_app
        data:
          title: "🛡️ Nuovo Backup"
          message: >
            Backup completato: {{ states('sensor.backup_guardian_ultimo_backup') }}
            Destinazione: {{ state_attr('sensor.backup_guardian_info_backup', 'backup_destination') }}
            Dimensione: {{ state_attr('sensor.backup_guardian_info_backup', 'backup_size') }}
```

### Alert Backup Vecchi

```yaml
automation:
  - alias: "Alert Backup Vecchi"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: template
        value_template: >
          {{ (now() - state_attr('sensor.backup_guardian_info_backup', 'backup_date') | as_datetime).days > 7 }}
    action:
      - service: notify.persistent_notification
        data:
          title: "⚠️ Backup Vecchio"
          message: "L'ultimo backup risale a più di 7 giorni fa!"
```

### Monitoraggio Spazio

```yaml
automation:
  - alias: "Alert Spazio Backup"
    trigger:
      - platform: numeric_state
        entity_id: sensor.backup_guardian_dimensione_totale
        above: 10000  # 10 GB
    action:
      - service: notify.mobile_app
        data:
          title: "💾 Spazio Backup Elevato"
          message: >
            I backup occupano {{ states('sensor.backup_guardian_dimensione_totale') }} MB.
            Considera di eliminare backup vecchi.
```

---

## 🐛 Troubleshooting

### Errore "Detected blocking call"

**Soluzione**: Questo è normale al primo avvio. Le librerie Google vengono scaricate. Aspetta 2-3 minuti e riavvia HA.

### Google Drive non mostra backup

**Verifica**:
1. Client ID e Secret corretti?
2. Folder ID corretto? (usa `root` se dubbi)
3. API Drive abilitata in Google Cloud Console?
4. Email aggiunta come utente test?
5. Token autorizzato correttamente?

**Debug**:
```
Impostazioni → Sistema → Log
Cerca: "backup_guardian"
```

### Card non si aggiorna

**Soluzione**:
1. Svuota cache browser (Ctrl+Shift+R)
2. iOS: Impostazioni app → Reimposta cache frontend
3. Riavvia Home Assistant

---

## 🤝 Contribuire

Contributi benvenuti! 

1. **Fork** il repository
2. Crea un **branch** per la tua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. Apri una **Pull Request**

---

## 📝 Roadmap

### v1.3.0 (Prossima)
- [ ] Integrazione Dropbox
- [ ] Integrazione OneDrive
- [ ] Backup automatico su schedule
- [ ] Pulizia automatica backup vecchi

### v1.4.0 (Futura)
- [ ] Supporto FTP/SFTP
- [ ] Supporto NAS (Synology, QNAP)
- [ ] Encryption backup
- [ ] Verifica integrità automatica

---

## 💝 Supporto

Se ti piace questo progetto, considera di supportarlo!

[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=flat-square)](https://paypal.me/leonardogarraffo)

Oppure:
- ⭐ Metti una stella su GitHub
- 🐛 Segnala bug
- 💡 Suggerisci features
- 📖 Migliora la documentazione

---

## 📄 Licenza

Questo progetto è distribuito con licenza **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

Puoi:
- ✅ Usarlo liberamente
- ✅ Modificarlo
- ✅ Condividerlo

**Non puoi**:
- ❌ Usarlo per scopi commerciali

Per maggiori dettagli: https://creativecommons.org/licenses/by-nc/4.0/

---

## 🙏 Ringraziamenti

- **Home Assistant Community** per il supporto
- **HACS** per la distribuzione
- Tutti i **contributor** e **tester**

---

## 📞 Contatti

- **Issues**: [GitHub Issues](https://github.com/leonardus1973/backup-guardian/issues)
- **Discussioni**: [GitHub Discussions](https://github.com/leonardus1973/backup-guardian/discussions)

---

**Made with ❤️ in Italy** 🇮🇹

**Backup Guardian** - *Perché i tuoi backup meritano un guardiano!* 🛡️

