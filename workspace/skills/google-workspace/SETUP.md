# gogcli Diegimo Instrukcija

## 1. Įdiegti Go
https://go.dev/dl/ (v1.21+)

## 2. Įdiegti gogcli

```bash
git clone https://github.com/steipete/gogcli.git
cd gogcli && make
# Sukompiliuotas binary → /usr/local/bin/gog arba ~/go/bin/gog
```

## 3. Google OAuth2 Credentials

1. Google Cloud Console → New Project → Enable APIs: Gmail, Drive, Calendar, Sheets
2. Credentials → Create OAuth 2.0 Client ID → Desktop App → Download JSON
3. Paleisti:
```bash
gog auth credentials ~/Downloads/client_secret_*.json
gog auth add user@gmail.com   # Atsidarys naršyklė OAuth patvirtinimui
```

## 4. Nanobot konfigūracija

Paleisti gateway su GOG_ACCOUNT:
```bash
GOG_ACCOUNT=user@gmail.com NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -m nanobot gateway
```

## 5. Patikrinimas

```bash
export GOG_ACCOUNT=user@gmail.com
gog gmail search 'newer_than:7d' --max 5 --json
```
