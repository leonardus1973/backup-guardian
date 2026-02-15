# 📝 Esempi di Configurazione - Backup Guardian v1.1.0

Questa guida contiene esempi pratici di come utilizzare Backup Guardian con automazioni e script.

## 📊 Uso Base dei Sensori

### Visualizzare Informazioni Ultimo Backup

```yaml
# In una card Entities o Markdown
type: entities
entities:
  - entity: sensor.backup_guardian_ultimo_backup
    name: Ultimo Backup
  - type: attribute
    entity: sensor.backup_guardian_ultimo_backup
    attribute: backup_name
    name: Nome Backup
  - type: attribute
    entity: sensor.backup_guardian_ultimo_backup
    attribute: backup_destination
    name: Destinazione
  - type: attribute
    entity: sensor.backup_guardian_ultimo_backup
    attribute: backup_size
    name: Dimensione
```

### Visualizzare Statistiche Backup

```yaml
# Card con statistiche
type: glance
entities:
  - entity: sensor.backup_guardian_totale_backup
    name: Totale Backup
  - entity: sensor.backup_guardian_dimensione_totale
    name: Spazio Occupato
```

---

## 🤖 Automazioni

### 1. Notifica Backup Mancante

Invia una notifica se non viene effettuato un backup da più di 7 giorni.

```yaml
automation:
  - alias: "Avviso Backup Mancante"
    description: "Notifica se non c'è un backup recente"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: template
        value_template: >
          {{ (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days > 7 }}
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "⚠️ Attenzione Backup"
          message: "Nessun backup effettuato da più di 7 giorni!"
          data:
            push:
              sound: "default"
              badge: 1
```

### 2. Notifica Nuovo Backup Completato

Invia una notifica quando viene completato un nuovo backup.

```yaml
automation:
  - alias: "Notifica Nuovo Backup"
    description: "Avvisa quando viene completato un backup"
    trigger:
      - platform: state
        entity_id: sensor.backup_guardian_ultimo_backup
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state != 'unknown' }}"
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "✅ Backup Completato"
          message: >
            Nuovo backup: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
            Destinazione: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_destination') }}
            Dimensione: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_size') }}
            Ora: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_time') }}
```

### 3. Notifica Spazio Backup Elevato

Avvisa quando lo spazio occupato dai backup supera una soglia.

```yaml
automation:
  - alias: "Avviso Spazio Backup Elevato"
    description: "Notifica quando i backup occupano più di 5GB"
    trigger:
      - platform: numeric_state
        entity_id: sensor.backup_guardian_dimensione_totale
        above: 5000
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "⚠️ Spazio Backup Elevato"
          message: >
            I backup occupano {{ states('sensor.backup_guardian_dimensione_totale') }} MB.
            Considera di eliminare i backup più vecchi.
```

### 4. Promemoria Backup Settimanale

Ricorda di fare un backup ogni domenica sera.

```yaml
automation:
  - alias: "Promemoria Backup Settimanale"
    description: "Ricorda di fare il backup settimanale"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "📦 Promemoria Backup"
          message: "È domenica sera, ricordati di fare il backup settimanale!"
```

### 5. Backup Automatico Notturno

Esegue automaticamente un backup completo ogni notte.

```yaml
automation:
  - alias: "Backup Automatico Notturno"
    description: "Backup automatico alle 3 di notte"
    trigger:
      - platform: time
        at: "03:00:00"
    action:
      - service: hassio.backup_full
        data:
          name: "Backup Automatico {{ now().strftime('%Y-%m-%d %H:%M') }}"
      - delay: "00:05:00"
      - service: notify.mobile_app_iphone
        data:
          title: "✅ Backup Automatico"
          message: "Backup notturno completato con successo"
```

### 6. Verifica Integrità Settimanale

Verifica l'integrità dei backup ogni settimana.

```yaml
automation:
  - alias: "Verifica Integrità Backup"
    description: "Controlla che tutti i backup abbiano un hash valido"
    trigger:
      - platform: time
        at: "10:00:00"
    condition:
      - condition: time
        weekday:
          - mon
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "🔍 Verifica Backup"
          message: >
            Backup totali: {{ states('sensor.backup_guardian_totale_backup') }}
            Ultimo backup: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
            Hash: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_hash')[:16] }}...
```

---

## 🎨 Card Personalizzate

### Card Markdown con Informazioni Dettagliate

```yaml
type: markdown
content: |
  ## 🛡️ Backup Guardian
  
  **Ultimo Backup:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
  **Destinazione:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_destination') }}
  **Data:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_date') }}
  **Ora:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_time') }}
  **Dimensione:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_size') }}
  
  ---
  
  **Backup Totali:** {{ states('sensor.backup_guardian_totale_backup') }}
  **Spazio Occupato:** {{ states('sensor.backup_guardian_dimensione_totale') }} MB
  
  **Hash SHA256:**  
  `{{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_hash')[:32] }}...`
title: Stato Backup
```

### Card Entities con Attributi

```yaml
type: entities
title: 🛡️ Backup Guardian
entities:
  - entity: sensor.backup_guardian_ultimo_backup
    name: Ultimo Backup
    icon: mdi:backup-restore
  - type: attribute
    entity: sensor.backup_guardian_ultimo_backup
    attribute: backup_destination
    name: Destinazione
    icon: mdi:map-marker
  - type: attribute
    entity: sensor.backup_guardian_ultimo_backup
    attribute: backup_size
    name: Dimensione
    icon: mdi:harddisk
  - type: divider
  - entity: sensor.backup_guardian_totale_backup
    name: Totale Backup
    icon: mdi:counter
  - entity: sensor.backup_guardian_dimensione_totale
    name: Spazio Totale
    icon: mdi:database
```

### Card Gauge per Spazio Occupato

```yaml
type: gauge
entity: sensor.backup_guardian_dimensione_totale
name: Spazio Backup
unit: MB
min: 0
max: 10000
severity:
  green: 0
  yellow: 5000
  red: 8000
```

---

## 📊 Dashboard Completa Backup

Esempio di dashboard dedicata ai backup:

```yaml
title: Backup
views:
  - title: Backup
    path: backup
    badges: []
    cards:
      - type: custom:backup-guardian-card
        entity: sensor.backup_guardian_totale_backup
        last_backup_entity: sensor.backup_guardian_ultimo_backup
        size_entity: sensor.backup_guardian_dimensione_totale
      
      - type: horizontal-stack
        cards:
          - type: gauge
            entity: sensor.backup_guardian_totale_backup
            name: Backup Totali
            min: 0
            max: 20
          - type: gauge
            entity: sensor.backup_guardian_dimensione_totale
            name: Spazio MB
            min: 0
            max: 10000
      
      - type: markdown
        content: |
          ## 📋 Lista Completa Backup
          
          {% for backup in state_attr('sensor.backup_guardian_totale_backup', 'backup_list') %}
          ### {{ loop.index }}. {{ backup.name }}
          - **Destinazione:** {{ backup.destination }}
          - **Data/Ora:** {{ backup.date }} {{ backup.time }}
          - **Dimensione:** {{ backup.size }}
          - **Hash:** `{{ backup.hash[:16] }}...`
          
          ---
          {% endfor %}
        title: Tutti i Backup
```

---

## 🔔 Notifiche Avanzate

### Notifica con Azioni (iOS)

```yaml
automation:
  - alias: "Backup Completato con Azioni"
    trigger:
      - platform: state
        entity_id: sensor.backup_guardian_ultimo_backup
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "✅ Backup Completato"
          message: >
            {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
            Dimensione: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_size') }}
          data:
            actions:
              - action: "VISUALIZZA_BACKUP"
                title: "Visualizza"
              - action: "IGNORA"
                title: "OK"
```

### Notifica Persistente (Android)

```yaml
automation:
  - alias: "Backup Status Persistente"
    trigger:
      - platform: state
        entity_id: sensor.backup_guardian_ultimo_backup
    action:
      - service: notify.mobile_app_android
        data:
          title: "📦 Backup Status"
          message: >
            Ultimo: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_time') }}
            Totale: {{ states('sensor.backup_guardian_totale_backup') }}
          data:
            tag: "backup_status"
            persistent: true
            sticky: true
```

---

## 📈 Template Sensor Personalizzati

### Sensor: Giorni dall'Ultimo Backup

```yaml
template:
  - sensor:
      - name: "Giorni dall'Ultimo Backup"
        unit_of_measurement: "giorni"
        state: >
          {% set last_backup = states('sensor.backup_guardian_ultimo_backup') %}
          {% if last_backup != 'unknown' %}
            {{ (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days }}
          {% else %}
            unknown
          {% endif %}
        icon: mdi:calendar-clock
```

### Sensor: Stato Backup (OK/Warning/Critical)

```yaml
template:
  - sensor:
      - name: "Stato Backup"
        state: >
          {% set days = (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days %}
          {% if days < 3 %}
            OK
          {% elif days < 7 %}
            Warning
          {% else %}
            Critical
          {% endif %}
        icon: >
          {% set days = (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days %}
          {% if days < 3 %}
            mdi:check-circle
          {% elif days < 7 %}
            mdi:alert
          {% else %}
            mdi:alert-circle
          {% endif %}
```

### Binary Sensor: Backup Recente

```yaml
template:
  - binary_sensor:
      - name: "Backup Recente"
        device_class: problem
        state: >
          {{ (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days > 7 }}
```

---

## 🔧 Script Utili

### Script: Verifica Backup

```yaml
script:
  verifica_backup:
    alias: "Verifica Status Backup"
    sequence:
      - service: persistent_notification.create
        data:
          title: "📦 Stato Backup"
          message: >
            **Ultimo Backup:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
            
            **Destinazione:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_destination') }}
            
            **Data/Ora:** {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_date') }} {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_time') }}
            
            **Backup Totali:** {{ states('sensor.backup_guardian_totale_backup') }}
            
            **Spazio Occupato:** {{ states('sensor.backup_guardian_dimensione_totale') }} MB
```

### Script: Crea Backup e Notifica

```yaml
script:
  crea_backup_completo:
    alias: "Crea Backup Completo"
    sequence:
      - service: hassio.backup_full
        data:
          name: "Backup Manuale {{ now().strftime('%Y-%m-%d %H:%M') }}"
      - delay: "00:02:00"
      - service: homeassistant.update_entity
        target:
          entity_id: sensor.backup_guardian_ultimo_backup
      - delay: "00:00:10"
      - service: notify.mobile_app_iphone
        data:
          title: "✅ Backup Creato"
          message: >
            Backup completato con successo!
            Destinazione: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_destination') }}
```

---

## 💡 Consigli Best Practice

1. **Backup Regolari**: Configura un'automazione per backup automatici notturni
2. **Monitoring**: Usa le notifiche per essere sempre informato
3. **Pulizia**: Elimina i backup vecchi periodicamente per liberare spazio
4. **Verifica**: Controlla settimanalmente l'integrità tramite hash SHA256
5. **Multi-destinazione**: Quando disponibile, usa backup cloud per ridondanza

---

**Per altre configurazioni o domande, apri un [Issue su GitHub](https://github.com/leonardus1973/backup-guardian/issues)!**

**Backup Guardian v1.1.0** - Esempi e Configurazioni
