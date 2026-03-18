# Journaling App - CLI Edition

Eine minimalistische Journaling-Anwendung mit CLI-Ästhetik, entwickelt mit Angular 21 und beruhigenden Farben.

## Features

- **Einfaches Interface**: Nur ein Titelfeld und ein großes Eingabefeld für deine Gedanken
- **CLI-Ästhetik**: Inspiriert von klassischen Terminal-Designs mit monospace Schriftart
- **Beruhigende Farben**: Dunkles Farbschema mit Cyan-Akzenten für entspanntes Schreiben
- **Lokale Speicherung**: Alle Einträge werden im Browser-LocalStorage gespeichert
- **Tastaturkürzel**: Drücke Ctrl+S, um deinen Eintrag zu speichern
- **Statistiken**: Zeigt die Anzahl der gespeicherten Einträge und den letzten Speicherzeitpunkt

## Farbschema

| Element | Farbe | Hex-Code |
|---------|-------|----------|
| Hintergrund | Dunkelblau | #0a0e27 |
| Text | Hellgrau | #a0aec0 |
| Akzente | Cyan | #4fd1c5 |
| Muted Text | Dunkelgrau | #2d3748 |

## Entwicklung

### Voraussetzungen

- Node.js 22.13.0 oder höher
- npm 10.9.2 oder höher

### Installation

```bash
cd journaling-app
npm install
```

### Entwicklungsserver starten

```bash
npm start
```

Öffne deinen Browser und navigiere zu `http://localhost:4200/`. Die Anwendung wird automatisch neu geladen, wenn du Dateien änderst.

### Produktion bauen

```bash
npm run build
```

Die Build-Artefakte werden im `dist/`-Verzeichnis gespeichert.

## Projektstruktur

```
journaling-app/
├── src/
│   ├── app/
│   │   ├── app.ts          # Hauptkomponente mit Journaling-Logik
│   │   └── app.config.ts   # Angular-Konfiguration
│   ├── main.ts             # Einstiegspunkt
│   ├── index.html          # HTML-Template
│   └── styles.css          # Globale Styles
├── dist/                   # Build-Output
├── package.json            # Abhängigkeiten
├── angular.json            # Angular-Konfiguration
└── tsconfig.json           # TypeScript-Konfiguration
```

## Verwendung

1. **Titel eingeben**: Gib einen Titel für deinen Eintrag in das erste Feld ein
2. **Schreiben**: Schreibe deine Gedanken im großen Textarea-Feld
3. **Speichern**: Klicke auf "Save Entry" oder drücke Ctrl+S
4. **Löschen**: Klicke auf "Clear", um den aktuellen Eintrag zu löschen

Alle Einträge werden automatisch im LocalStorage gespeichert und bleiben erhalten, auch wenn du die Seite neu lädst.

## Technologie-Stack

- **Framework**: Angular 21
- **Sprache**: TypeScript
- **Styling**: CSS mit Inline-Styles
- **Speicherung**: Browser LocalStorage

## Lizenz

Dieses Projekt wurde mit Angular CLI generiert.
