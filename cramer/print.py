from collections.abc import Iterable
from typing import Dict, List

import json
import toml

from .coal import Coal
from github.Commit import Commit

def print_text(result: Coal):
	print(f"Head: {result.head_branch_name}")
	print(f"Base: {result.target_branch_name}")
	print("Found:")
	for found in result.commits_in_target:
		print(f"\tsha: {found.sha} message: {found.commit.message} url: {found.html_url}")

	if result.commits_not_found:
		print("Missing:")
		for missing in result.commits_not_found:
			print(f"\tsha: {missing.sha} message: {missing.commit.message} url: {found.html_url}")




def extract_commit_info(commits: Iterable[Commit]) -> List[Dict[str, str]]:
	return [{ "sha": commit.sha, "message": commit.commit.message, "url": commit.html_url } for commit in commits]


def get_result_dict(result: Coal) -> dict:
	return {
		"head": result.head_branch_name,
		"base": result.target_branch_name,
		"found": extract_commit_info(result.commits_in_target),
		"missing": extract_commit_info(result.commits_not_found),
	}

def print_json(result: Coal):
	print(json.dumps(get_result_dict(result), indent=4))


def print_toml(result: Coal):
	print(toml.dumps(get_result_dict(result)))