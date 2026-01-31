# Esempi di Configurazione - Backup Guardian

## 1. Card Base

```yaml
type: custom:backup-guardian-card
entity: sensor.totale_backup
last_backup_entity: sensor.ultimo_backup
```

## 2. Configurazione Lovelace Resources

### Metodo A: configuration.yaml
```yaml
lovelace:
  mode: yaml
  resources:
    - url: /local/community/backup_guardian/backup-guardian-card.js
      type: module
```

### Metodo B: UI
1. Impostazioni → Dashboard → Risorse
2. + Aggiungi risorsa
3. URL: `/local/community/backup_guardian/backup-guardian-card.js`
4. Tipo: Modulo JavaScript

## 3. Automazioni Utili

### Notifica Backup Giornaliero
```yaml
automation:
  - alias: "Notifica Backup Completato"
    trigger:
      - platform: state
        entity_id: sensor.ultimo_backup
    action:
      - service: notify.mobile_app_il_tuo_telefono
        data:
          title: "✅ Backup Completato"
          message: >
            Nuovo backup: {{ state_attr('sensor.ultimo_backup', 'backup_name') }}
            Dimensione: {{ state_attr('sensor.ultimo_backup', 'backup_size') }}
```

### Avviso Backup Vecchi
```yaml
automation:
  - alias: "Avviso Nessun Backup Recente"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: template
        value_template: >
          {% set last_backup = states('sensor.ultimo_backup') %}
          {% if last_backup != 'Nessun backup' %}
            {% set backup_date = strptime(state_attr('sensor.ultimo_backup', 'backup_date'), '%Y-%m-%d') %}
            {{ (now() - backup_date).days > 7 }}
          {% else %}
            true
          {% endif %}
    action:
      - service: notify.persistent_notification
        data:
          title: "⚠️ Attenzione Backup"
          message: "Non viene effettuato un backup da più di 7 giorni!"
```

### Pulizia Automatica Backup Vecchi
```yaml
automation:
  - alias: "Pulizia Backup Vecchi"
    trigger:
      - platform: time
        at: "03:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.totale_backup
        above: 10
    action:
      - service: persistent_notification.create
        data:
          title: "🗑️ Pulizia Backup"
          message: "Hai più di 10 backup. Considera di eliminare quelli più vecchi."
```

## 4. Card con Template

### Card Entities con Sensori
```yaml
type: entities
title: Stato Backup
entities:
  - entity: sensor.ultimo_backup
    name: Ultimo Backup
    icon: mdi:backup-restore
  - entity: sensor.totale_backup
    name: Totale Backup
    icon: mdi:counter
  - entity: sensor.dimensione_totale_backup
    name: Spazio Occupato
    icon: mdi:harddisk
    unit_of_measurement: MB
```

### Glance Card
```yaml
type: glance
title: Backup Status
entities:
  - entity: sensor.ultimo_backup
    name: Ultimo
  - entity: sensor.totale_backup
    name: Totale
  - entity: sensor.dimensione_totale_backup
    name: Dimensione
```

## 5. Script Utili

### Verifica Spazio Backup
```yaml
script:
  check_backup_space:
    alias: "Verifica Spazio Backup"
    sequence:
      - service: persistent_notification.create
        data:
          title: "💾 Spazio Backup"
          message: >
            Backup totali: {{ states('sensor.totale_backup') }}
            Spazio occupato: {{ states('sensor.dimensione_totale_backup') }} MB
            Ultimo backup: {{ states('sensor.ultimo_backup') }}
```

## 6. Dashboard Completa

```yaml
views:
  - title: Backup
    icon: mdi:shield-check
    cards:
      - type: custom:backup-guardian-card
        entity: sensor.totale_backup
        last_backup_entity: sensor.ultimo_backup
      
      - type: entities
        title: Dettagli Backup
        entities:
          - entity: sensor.ultimo_backup
          - entity: sensor.totale_backup
          - entity: sensor.dimensione_totale_backup
      
      - type: markdown
        content: >
          ## Stato Backup
          
          **Ultimo backup:** {{ states('sensor.ultimo_backup') }}
          
          **Hash SHA256:** {{ state_attr('sensor.ultimo_backup', 'backup_hash')[:16] }}...
```

## 7. Logger per Debug

```yaml
logger:
  default: info
  logs:
    custom_components.backup_guardian: debug
```

## 8. Conditional Card

### Mostra solo se ci sono backup
```yaml
type: conditional
conditions:
  - entity: sensor.totale_backup
    state_not: "0"
card:
  type: custom:backup-guardian-card
  entity: sensor.totale_backup
  last_backup_entity: sensor.ultimo_backup
```

### Alert se nessun backup
```yaml
type: conditional
conditions:
  - entity: sensor.totale_backup
    state: "0"
card:
  type: markdown
  content: |
    ## ⚠️ Attenzione!
    Nessun backup trovato!
```

## Note

- Riavvia sempre Home Assistant dopo aver modificato `configuration.yaml`
- Svuota la cache del browser dopo aver aggiunto nuove risorse
- I sensori si aggiornano ogni 5 minuti di default
