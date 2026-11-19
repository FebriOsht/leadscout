<p align="center">
  <a href="https://lab.vulpfest.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-night.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-day.svg" />
      <img src="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-night.svg" height="44" alt="Vulpfest Lab" />
    </picture>
  </a>
</p>
# LeadScout

Research B2B prospects from public search results.

**Try it online:** [lab.vulpfest.com/leadscout](https://lab.vulpfest.com/leadscout), part of [Vulpfest Lab](https://lab.vulpfest.com), free and open-source tools from Vulpfest.

## What it does

- Describe the kind of company you are looking for and run a search over public web results.
- Builds a tidy list of potential prospects with publicly available company information.
- Export the list to share with your sales team.

## Run it yourself

```bash
git clone https://github.com/FebriOsht/leadscout.git
cd leadscout
pip install -r requirements.txt
streamlit run app.py
```

## Works on Windows, macOS and Linux

Requires Python 3.10 or newer. A virtual environment keeps the packages separate from the rest of your system.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS and Linux (bash or zsh)**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If PowerShell blocks the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

## Command line

```bash
pip install ddgs
python cli.py --roles "software house, IT consultant" --industries "technology" --location "Jakarta" --out prospects.csv
```

| Option | Meaning |
|---|---|
| `--roles` | comma-separated roles or keywords (required) |
| `--industries` | comma-separated industry keywords (required; the first one is used in each search) |
| `--location` | optional location |
| `--source` | `web` (default) or `linkedin` |
| `--max` | maximum results per keyword, 1 to 50 (default 10) |
| `--campaign` | campaign name stored with each result |
| `--out` | save the results as CSV; without it, results are printed to the terminal |

## Responsible use

Use it for publicly available company information only, respect the terms and rate limits of the search services involved, and follow data protection laws such as Indonesia's Personal Data Protection Law (UU PDP) or the GDPR when you store any personal data.

The software is provided as is, without warranty. You are responsible for how you use it and for any data you collect.

## Security

Found a security issue? Please see [SECURITY.md](SECURITY.md).

## Support this project

This tool is free. If it saves you time, you can support its development:

- [Saweria](https://saweria.co/FebriOsht): QRIS, e-wallet and bank transfer, for supporters in Indonesia
- [PayPal](https://paypal.me/FebriOsht)
- Crypto (USDT BEP20, USDT TRC20, Bitcoin): see the [addresses and QR codes](https://github.com/FebriOsht#support)

Starring the repository helps too. ⭐

## License

MIT © 2026 Febri Osht (Vulpfest). See [LICENSE](LICENSE).