# 🚀 Guida Rapida - Backup Guardian v1.1.0

## Installazione in 3 Passi

### 📥 Passo 1: Installa l'Integrazione

**Via HACS (Consigliato)**
1. HACS → Integrazioni
2. Tre puntini → Repository personalizzati
3. URL: `https://github.com/leonardus1973/backup-guardian`
4. Categoria: Integration
5. Installa "Backup Guardian"
6. **RIAVVIA HOME ASSISTANT**

✅ Il file JavaScript viene copiato automaticamente!

**Via Manuale**
1. Scarica `custom_components/backup_guardian`
2. Copia in `/config/custom_components/backup_guardian/`
3. **RIAVVIA HOME ASSISTANT**

✅ Il file JavaScript viene copiato automaticamente al primo avvio!

---

### ⚙️ Passo 2: Configura l'Integrazione

1. **Impostazioni** → **Dispositivi e servizi**
2. **+ Aggiungi integrazione**
3. Cerca "**Backup Guardian**"
4. Clicca **Invia**

✅ Fatto! I 3 sensori sono ora attivi:
- `sensor.backup_guardian_ultimo_backup`
- `sensor.backup_guardian_totale_backup`
- `sensor.backup_guardian_dimensione_totale`

---

### 🎨 Passo 3: Aggiungi la Lovelace Card

#### A. Registra la Risorsa JavaScript

1. **Impostazioni** → **Dashboard** → **Risorse**
2. **+ Aggiungi risorsa**
3. URL: `/local/community/backup_guardian/backup-guardian-card.js`
4. Tipo: **Modulo JavaScript**
5. **Crea**
6. **Svuota cache**: Ctrl+Shift+R (o Cmd+Shift+R su Mac)

#### B. Aggiungi la Card

1. Dashboard → **Modifica**
2. **+ Aggiungi Card** → **Manuale**
3. Incolla:

```yaml
type: custom:backup-guardian-card
entity: sensor.backup_guardian_totale_backup
last_backup_entity: sensor.backup_guardian_ultimo_backup
size_entity: sensor.backup_guardian_dimensione_totale
```

4. **Salva**

---

## ✅ Verifica Finale

Dovresti vedere:
- ✅ 📦 Ultimo Backup con badge **[HOME ASSISTANT LOCALE]**
- ✅ Statistiche (numero backup + MB totali)
- ✅ Bottone "Mostra Tutti i Backup" espandibile
- ✅ Lista con badge destinazione per ogni backup
- ✅ Orari corretti (non più -1h!)

---

## 🎯 Esempi di Uso

### Automazione: Notifica Backup Mancante

```yaml
automation:
  - alias: "Avviso Backup Mancante"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: template
        value_template: >
          {{ (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days > 7 }}
    action:
      - service: notify.mobile_app
        data:
          message: "⚠️ Nessun backup da più di 7 giorni!"
```

### Automazione: Notifica Nuovo Backup

```yaml
automation:
  - alias: "Notifica Nuovo Backup"
    trigger:
      - platform: state
        entity_id: sensor.backup_guardian_ultimo_backup
    action:
      - service: notify.mobile_app
        data:
          title: "✅ Backup Completato"
          message: >
            {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
            Destinazione: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_destination') }}
```

---

## 🐛 Problemi Comuni

### ❌ La card non appare?

1. **Svuota cache**: Ctrl+Shift+R (più volte!)
2. **Chiudi browser** completamente e riapri
3. **Prova incognito**: Verifica che sia un problema di cache
4. Verifica che il file esista: `/config/www/community/backup_guardian/backup-guardian-card.js`
5. Se manca, riavvia HA (viene copiato automaticamente)

### ❌ "Custom element doesn't exist"?

1. Verifica URL risorsa: `/local/community/backup_guardian/backup-guardian-card.js`
2. **Svuota cache completamente**:
   - Chrome/Edge: `edge://settings/clearBrowserData`
   - Seleziona "Immagini e file memorizzati nella cache"
   - Cancella tutto
3. Chiudi e riapri browser

### ❌ Sensori vuoti o N/A?

1. Verifica di essere su **HA OS** o **Supervised**
2. Controlla log: Impostazioni → Sistema → Log
3. Cerca `backup_guardian`
4. **Ricarica integrazione**: Dispositivi e Servizi → Backup Guardian → Tre puntini → Ricarica

### ❌ Orari sbagliati (-1h)?

Aggiorna alla v1.1.0! Questo bug è stato risolto.

### ❌ Badge destinazione non appaiono?

1. Verifica versione: deve essere **v1.1.0** o superiore
2. Svuota cache browser completamente
3. Verifica attributo:
   - Strumenti per sviluppatori → Stati
   - `sensor.backup_guardian_ultimo_backup`
   - Deve esserci `backup_destination: Home Assistant Locale`

---

## 💡 Suggerimento PRO

**Problema cache ostinato?**
1. Usa **modalità incognito** per verificare che il file sia corretto
2. Se funziona in incognito, il problema è la cache normale
3. Svuota cache completamente e riavvia browser

---

## 📊 Cosa Include la v1.1.0?

- ✅ **Copia automatica** file JavaScript (zero configurazione!)
- ✅ **Badge destinazione** per ogni backup
- ✅ **Orari corretti** (fix timezone)
- ✅ **Struttura multi-destinazione** (pronta per future integrazioni)
- ✅ **Compatibilità Python 3.13**
- ✅ **Gestione robusta** date e dimensioni

---

## 📞 Supporto

🐛 Bug? [Apri Issue](https://github.com/leonardus1973/backup-guardian/issues)  
💡 Idee? [Feature Request](https://github.com/leonardus1973/backup-guardian/issues)  
⭐ Ti piace? Lascia una stella su GitHub!

---

## 🔜 Prossimi Sviluppi

- 🌐 Google Drive backup
- 📦 Dropbox backup
- ☁️ OneDrive backup
- 📊 Grafici storici
- 🤖 Pulizia automatica
- ✅ Verifica integrità

---

**Installazione completata in 5 minuti! 🎉**

**Backup Guardian v1.1.0** - Prima versione stabile e completa!
