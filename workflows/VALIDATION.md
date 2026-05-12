# Validation Notes

Validated locally on 2026-05-13.

## Static Workflow Validation

```bash
python3 tests/validate_n8n_workflow.py
```

Result:

```text
Validated workflows/github-weekly-summary.workflow.json: 10 nodes, cron 0 17 * * 5
```

This checks:

- Importable JSON syntax
- Required n8n nodes
- Friday 5pm weekly cron
- GitHub commits, issues, and pulls API paths
- Claude model `claude-sonnet-4-20250514`
- Configurable `GITHUB_REPO`, `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, `DISCORD_WEBHOOK_URL`, and `SUMMARY_LANGUAGE`

## n8n CLI Import

```bash
N8N_USER_FOLDER=/tmp/n8n-claude-builders-5 \
  npx --yes n8n@latest import:workflow \
  --input=workflows/github-weekly-summary.workflow.json
```

Result: command completed with exit code `0`.

Live end-to-end execution requires real GitHub, Anthropic, and Discord credentials. The workflow is configured to run manually in n8n for that final smoke test before activation.
