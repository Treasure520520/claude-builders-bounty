#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "workflows" / "github-weekly-summary.workflow.json"


def main() -> int:
    data = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    nodes = {node["name"]: node for node in data["nodes"]}
    required_nodes = [
        "Weekly Trigger",
        "Configuration",
        "Normalize Config",
        "Fetch Commits",
        "Fetch Closed Issues",
        "Fetch Merged PRs",
        "Build Claude Prompt",
        "Call Claude API",
        "Format Discord Payload",
        "Send to Discord",
    ]
    missing = [name for name in required_nodes if name not in nodes]
    assert not missing, f"Missing nodes: {missing}"

    trigger = nodes["Weekly Trigger"]
    cron = trigger["parameters"]["rule"]["interval"][0]["expression"]
    assert cron == "0 17 * * 5", f"Unexpected cron: {cron}"

    claude_body = nodes["Call Claude API"]["parameters"]["jsonBody"]
    assert "claude-sonnet-4-20250514" in claude_body

    config_text = json.dumps(nodes["Configuration"])
    for key in ["GITHUB_REPO", "GITHUB_TOKEN", "ANTHROPIC_API_KEY", "DISCORD_WEBHOOK_URL", "SUMMARY_LANGUAGE"]:
        assert key in config_text, f"Missing configurable variable {key}"

    github_urls = "\n".join(
        node["parameters"].get("url", "")
        for node in data["nodes"]
        if node["type"] == "n8n-nodes-base.httpRequest"
    )
    for path in ["/commits", "/issues", "/pulls"]:
        assert path in github_urls, f"Missing GitHub API path {path}"

    connections = data["connections"]
    for source in required_nodes[:-1]:
        assert source in connections, f"Missing connection from {source}"

    print(f"Validated {WORKFLOW}: {len(data['nodes'])} nodes, cron {cron}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
