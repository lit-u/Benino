---
name: google-workspace
description: Naudoti Gmail, Google Drive, Calendar, Sheets ir Contacts per gogcli CLI. Veiksmams: tikrinti el. paštą, siųsti žinutes, skaityti/įkelti failus į Drive, peržiūrėti/kurti kalendoriaus įvykius, skaityti/atnaujinti Sheets lentas.
always: false
---

# Google Workspace Skill

Naudok `exec` įrankį su `gog.exe` komandomis.

## Konfigūracija
- **gog.exe kelias:** `C:/Users/Herba/bin/gog.exe`
- **Paskyra:** `herbertas.a@gmail.com`
- Visada pridėk `--account herbertas.a@gmail.com` arba naudok `GOG_ACCOUNT=herbertas.a@gmail.com`

## Gmail

```bash
# Neperskaityti laiškai
exec(command="C:/Users/Herba/bin/gog.exe gmail search 'is:unread' --max 10 --json")

# Ieškoti laiškų
exec(command="C:/Users/Herba/bin/gog.exe gmail search 'newer_than:7d' --max 10 --json")

# Siųsti laišką
exec(command="C:/Users/Herba/bin/gog.exe gmail send --to gavėjas@example.com --subject 'Tema' --body 'Tekstas'")
```

## Google Drive

```bash
# Failų sąrašas
exec(command="C:/Users/Herba/bin/gog.exe drive ls --max 20 --json")

# Ieškoti failo
exec(command="C:/Users/Herba/bin/gog.exe drive search 'pavadinimas' --max 10 --json")

# Įkelti failą
exec(command="C:/Users/Herba/bin/gog.exe drive upload ./failas.pdf")
```

## Google Calendar

```bash
# Šiandienos įvykiai
exec(command="C:/Users/Herba/bin/gog.exe calendar events primary --today --json")

# Kurti įvykį
exec(command="C:/Users/Herba/bin/gog.exe calendar create primary --summary 'Susitikimas' --from 2026-03-01T10:00:00Z --to 2026-03-01T11:00:00Z")
```

## Google Sheets

```bash
# Nuskaityti langelius
exec(command="C:/Users/Herba/bin/gog.exe sheets get SPREADSHEET_ID 'Sheet1!A1:D10' --json")

# Atnaujinti langelį
exec(command="C:/Users/Herba/bin/gog.exe sheets update SPREADSHEET_ID 'A1' 'Reikšmė'")
```

## Svarbu
- Visada naudok `--json` read operacijoms
- Diegimo instrukcija: `workspace/skills/google-workspace/SETUP.md`
