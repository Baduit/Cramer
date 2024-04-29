from collections.abc import Iterable
from typing import Dict, List

import json
import toml

from rich import box
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from .coal import Coal
from github.Commit import Commit


def print_rich(result: Coal):
	console = Console()
	tree = Tree("")

	branches_branch = tree.add(":evergreen_tree: Branches")

	head_branch = branches_branch.add(":exploding_head: Head")
	head_branch.add(f"[bold]{result.head_branch_name}[/bold]")

	head_branch = branches_branch.add(":dart: Base")
	head_branch.add(f"[bold]{result.target_branch_name}[/bold]")

	commit_branch = tree.add(":memo: [bold]Commits[/bold]")
	# Found
	found_table = Table(show_header=True, header_style="bold green", show_lines=True)
	found_table.add_column("Sha")
	found_table.add_column("Commit message")
	found_table.add_column("Github url")
	found_table.box = box.SQUARE_DOUBLE_HEAD
	for commit in result.commits_in_target:
		found_table.add_row(commit.sha, commit.commit.message, f"[blue]{commit.html_url}[/blue]")
	found_branch = commit_branch.add(":green_circle: [green]Found[/green]")
	found_branch.add(found_table)

	# Missing
	if result.commits_not_found:
		missing_table = Table(show_header=True, header_style="bold red", show_lines=True)
		missing_table.add_column("Sha")
		missing_table.add_column("Commit message")
		missing_table.add_column("Github url")
		missing_table.box = box.SQUARE_DOUBLE_HEAD
		for commit in result.commits_not_found:
			missing_table.add_row(commit.sha, commit.commit.message, f"[blue]{commit.html_url}[/blue]")
		missing_branch = commit_branch.add(":red_circle: [red]Missing[/red]")
		missing_branch.add(missing_table)

	console.print(tree)


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
