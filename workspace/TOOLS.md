# TOOLS.md — Projekto Keliai ir Komandos

## Svarbūs Keliai (Windows → forward slashes)
- Config: `C:/Users/Herba/.nanobot/config.json`
- Workspace: `d:/_PAL/benino/workspace/`
- Agent Network: `d:/_PAL/benino/agent-network/`

## Pagrindinės exec() Komandos
```
sutvarkyk:  node d:/_PAL/benino/agent-network/sutvarkyk.js [URL]
git push:   cd d:/_PAL/benino/agent-network && git add -u && git commit -m "..." && git push origin main
gog:        GOG_ACCOUNT=herbertas.a@gmail.com C:/Users/Herba/bin/gog.exe [komanda]
```

## Atmintis — Kada Ką Rašyti
| Turinys | Failas |
|---------|--------|
| Kritiniai faktai | `memory/MEMORY.md` |
| Šiandienos darbas | `memory/YYYY-MM-DD.md` |
| Projekto etapas | `memory/projects-log.md` |
| Klaida + fix | `memory/lessons.md` |

## Cron Sintaksė
```
delay_seconds=3600  |  every_seconds=3600  |  cron_expr="0 8 * * *"
```
