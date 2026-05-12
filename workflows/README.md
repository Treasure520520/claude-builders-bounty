# GitHub Weekly Narrative Summary

This n8n workflow generates a weekly narrative summary for a GitHub repository with Claude Sonnet 4 and posts it to Discord.

## Setup

1. Import `github-weekly-summary.workflow.json` into n8n.
2. Set environment variables: `GITHUB_REPO=owner/repo`, `GITHUB_TOKEN=...`, `ANTHROPIC_API_KEY=...`, `DISCORD_WEBHOOK_URL=...`, and `SUMMARY_LANGUAGE=EN` or `FR`.
3. Open the workflow and confirm the **Weekly Trigger** cron is `0 17 * * 5` for Friday 5pm.
4. Run **Execute workflow** once to verify GitHub fetch, Claude summary generation, and Discord delivery.
5. Activate the workflow.

## What It Does

- Runs every Friday at 5pm.
- Fetches commits, closed issues, and merged pull requests from the GitHub API for the last seven days.
- Calls Claude with `claude-sonnet-4-20250514`.
- Delivers the generated narrative summary to Discord.
- Supports English and French output through `SUMMARY_LANGUAGE`.

## Validation

The workflow structure can be checked locally without secrets:

```bash
python3 tests/validate_n8n_workflow.py
```

The workflow was also imported with the n8n CLI; see [`VALIDATION.md`](VALIDATION.md).

Live execution requires real `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, and `DISCORD_WEBHOOK_URL` values in an n8n instance.
