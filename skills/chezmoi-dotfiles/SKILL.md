---
name: chezmoi-dotfiles
description: Secure dotfiles management with chezmoi. Use when helping users initialize chezmoi repositories, add/manage dotfiles, handle secrets with age encryption, create templates for multi-machine configs, troubleshoot chezmoi issues, or review dotfiles for security. Always checks for security implications before adding files.
version: 1
triggers: ["chezmoi", "dotfiles", "encrypt", "age encryption", "template"]
---

<skill>
<objective>
Provide expert guidance for managing dotfiles securely with chezmoi, focusing on security-first practices, multi-machine synchronization, and proper secrets management.
</objective>

<quick_start>
Use `scripts/executable_init_chezmoi_repo.sh` to start a new repo. Add files with `chezmoi add`. Use `--encrypt` for secrets and `--template` for dynamic content. Run `scripts/executable_check_secrets.py` before committing.
</quick_start>

<success_criteria>
- Dotfiles are managed without exposing plaintext secrets in the repository
- Sensitive files (private keys, etc.) use age encryption
- Multi-machine configurations use templates and local `chezmoi.yaml` data
- The repository passes security audits and secret scans
</success_criteria>

<security_first_workflow>
1. **Contains secrets?** (API keys, passwords, keys)
   - YES -> Use age encryption or externalize to local `chezmoi.yaml`.
   - NO -> Proceed to step 2.
2. **Mixes secrets with public config?**
   - YES -> Use templates to separate concerns.
   - NO -> Proceed to step 3.
3. **Safe to add?**
   - YES -> Check `.chezmoiignore` patterns and use `chezmoi add`.
   - Run `scripts/executable_check_secrets.py` before every commit.
</security_first_workflow>

<essential_commands>
```bash
chezmoi init [repo-url]
chezmoi add ~/.bashrc
chezmoi add --template ~/.gitconfig
chezmoi add --encrypt ~/.ssh/id_ed25519
chezmoi diff
chezmoi apply -v
chezmoi update -v
chezmoi managed
```
</essential_commands>

<proactive_security_guidance>
- ⚠️ **.env files**: Add to `.chezmoiignore` instead of tracking.
- ⚠️ **SSH keys**: Always use age encryption: `chezmoi add --encrypt`.
- ⚠️ **Mixed content**: Use templates with variables stored in local `chezmoi.yaml`.
- ⚠️ **Pre-commit**: Always run `scripts/executable_check_secrets.py`.
</proactive_security_guidance>

<resources>
<reference_index>
- **references/core-workflows.md**: Initialization, adding files, secrets, templates, and multi-machine setup
- **references/security-checklist.md**: Comprehensive security practices and audit procedures
- **references/ignore-patterns.md**: Extensive catalog of `.chezmoiignore` patterns
- **references/template-examples.md**: Practical template examples for Git, SSH, and Shell
- **references/chezmoi-commands.md**: Complete command reference
</reference_index>

<scripts_index>
- **scripts/executable_check_secrets.py**: Scan for potential secrets before committing
- **scripts/executable_init_chezmoi_repo.sh**: Initialize with security defaults
- **scripts/executable_generate_chezmoiignore.py**: Generate comprehensive ignore patterns
</scripts_index>

<assets_index>
- **assets/dot_chezmoiignore.template**: Starter ignore file
- **assets/dot_chezmoidata.yaml.template**: Starter template data
- **assets/README.md.template**: Documentation template
</assets_index>
</resources>
</skill>


---
# Additional Documentation from Legacy Version

