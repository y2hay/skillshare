# Chezmoi Core Workflows

## 1. Initialize New Chezmoi Repository
**Steps:**
```bash
# 1. Run initialization script (creates secure defaults)
bash scripts/init_chezmoi_repo.sh

# 2. Set up age encryption (recommended)
age-keygen -o ~/.config/chezmoi/key.txt

# Note the public key, then configure ~/.config/chezmoi/chezmoi.yaml:
encryption: "age"
age:
  identity: "${HOME}/.config/chezmoi/key.txt"
  recipient: "age1..."  # Public key from key.txt
```

## 2. Adding Dotfiles
**Security Decision Tree:**
- Shell config -> Add normally or template
- Git config -> Template for email
- SSH private key -> `chezmoi add --encrypt`
- .env file -> NEVER ADD (use .chezmoiignore)

**Commands:**
```bash
chezmoi add ~/.bashrc
chezmoi add --template ~/.gitconfig
chezmoi add --encrypt ~/.ssh/id_ed25519
```

## 3. Managing Secrets
- **Option A: Age Encryption**: `chezmoi add --encrypt` (Best for keys)
- **Option B: Templates + External Config**: Use variables in templates, store actual values in local `chezmoi.yaml`.
- **Option C: Don't Track**: Add to `.chezmoiignore`.

## 4. Creating Templates
**Scenarios:**
- **Git Config**: Use `{{ .git.email }}`
- **OS-Specific**: `{{- if eq .chezmoi.os "darwin" }}`
- **Machine-Specific**: `{{- if eq .machine.type "work" }}`

## 5. Multi-Machine Setup
1. Install chezmoi
2. `chezmoi init https://github.com/user/dotfiles.git`
3. Configure local `chezmoi.yaml` with machine-specific data
4. `chezmoi apply -v`

## 6. Security Audit
```bash
python3 scripts/check_secrets.py
git log -p | grep -E "api[_-]?key|password|secret"
chezmoi managed | grep -E "(\.env|credentials|secret)"
```

## 7. Troubleshooting
- **File not updating**: Check if managed/ignored, view `chezmoi diff`.
- **Template error**: Use `chezmoi cat` to preview, `chezmoi data` to view variables.
- **Encryption error**: Verify age key exists and `chezmoi.yaml` configuration.
