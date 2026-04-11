#!/usr/bin/env python3
"""Create GitHub labels, milestones, and issues from a local backlog manifest.

Usage:
    GITHUB_TOKEN=... python scripts/create_github_backlog.py --repo owner/name
    GITHUB_TOKEN=... python scripts/create_github_backlog.py --repo owner/name --apply

Without --apply, the script runs in dry-run mode and prints the actions it would take.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path("planning/github/astrosdk_2_0_backlog.json")
API_ROOT = "https://api.github.com"


def build_request(
    path: str,
    token: str,
    method: str = "GET",
    data: dict[str, Any] | None = None,
) -> urllib.request.Request:
    url = f"{API_ROOT}{path}"
    payload = None if data is None else json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, data=payload, method=method)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if payload is not None:
        request.add_header("Content-Type", "application/json")
    return request


def api_request(
    path: str,
    token: str,
    method: str = "GET",
    data: dict[str, Any] | None = None,
) -> Any:
    request = build_request(path, token, method=method, data=data)
    with urllib.request.urlopen(request) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if body else None


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_label(
    repo: str,
    label: dict[str, str],
    existing_labels: set[str],
    token: str,
    apply: bool,
) -> None:
    name = label["name"]
    if name in existing_labels:
        print(f"label exists: {name}")
        return
    print(f"create label: {name}")
    if apply:
        api_request(f"/repos/{repo}/labels", token, method="POST", data=label)
        existing_labels.add(name)


def fetch_existing_labels(repo: str, token: str) -> set[str]:
    labels = api_request(f"/repos/{repo}/labels?per_page=100", token)
    return {label["name"] for label in labels}


def fetch_existing_milestones(repo: str, token: str) -> dict[str, int]:
    milestones = api_request(f"/repos/{repo}/milestones?state=all&per_page=100", token)
    return {milestone["title"]: milestone["number"] for milestone in milestones}


def fetch_existing_issues(repo: str, token: str) -> set[str]:
    issues = api_request(
        f"/repos/{repo}/issues?state=all&per_page=100&filter=all", token
    )
    return {
        issue["title"]
        for issue in issues
        if "pull_request" not in issue
    }


def ensure_milestone(
    repo: str,
    milestone: dict[str, Any],
    existing_milestones: dict[str, int],
    token: str,
    apply: bool,
) -> int | None:
    title = milestone["title"]
    if title in existing_milestones:
        print(f"milestone exists: {title}")
        return existing_milestones[title]

    print(f"create milestone: {title}")
    if not apply:
        return None

    created = api_request(
        f"/repos/{repo}/milestones",
        token,
        method="POST",
        data={
            "title": milestone["title"],
            "description": milestone["description"],
        },
    )
    number = int(created["number"])
    existing_milestones[title] = number
    return number


def ensure_issue(
    repo: str,
    issue: dict[str, Any],
    milestone_number: int | None,
    existing_issues: set[str],
    token: str,
    apply: bool,
) -> None:
    title = issue["title"]
    if title in existing_issues:
        print(f"issue exists: {title}")
        return

    print(f"create issue: {title}")
    if not apply:
        return

    payload: dict[str, Any] = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue.get("labels", []),
    }
    if milestone_number is not None:
        payload["milestone"] = milestone_number

    api_request(f"/repos/{repo}/issues", token, method="POST", data=payload)
    existing_issues.add(title)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to the backlog manifest JSON file.",
    )
    parser.add_argument(
        "--repo",
        help="Target GitHub repository in owner/name format. Overrides manifest repo if provided.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually create labels, milestones, and issues. Without this flag, the script is dry-run only.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    repo = args.repo or manifest.get("repo")
    if not repo:
        print("error: repository is required via --repo or manifest", file=sys.stderr)
        return 1

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("error: GITHUB_TOKEN environment variable is required", file=sys.stderr)
        return 1

    print(f"target repo: {repo}")
    print("mode: apply" if args.apply else "mode: dry-run")

    try:
        existing_labels = fetch_existing_labels(repo, token)
        existing_milestones = fetch_existing_milestones(repo, token)
        existing_issues = fetch_existing_issues(repo, token)

        for label in manifest.get("labels", []):
            ensure_label(repo, label, existing_labels, token, apply=args.apply)

        for milestone in manifest.get("milestones", []):
            milestone_number = ensure_milestone(
                repo,
                milestone,
                existing_milestones,
                token,
                apply=args.apply,
            )
            for issue in milestone.get("issues", []):
                ensure_issue(
                    repo,
                    issue,
                    milestone_number,
                    existing_issues,
                    token,
                    apply=args.apply,
                )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"github api error: {exc.code} {exc.reason}", file=sys.stderr)
        print(body, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
