from dataclasses import dataclass
from typing import List, Set

import click
from github import Auth, Github, Commit, Consts
from github.Commit import Commit

from .coal import Coal
from .print import print_json, print_text, print_toml


def read_token(token_path: str) -> str:
	with open(token_path, "r") as f:
		return f.read()


def cmp_commit(left: Commit, right: Commit) -> bool:
	left_patches = [patch.patch for patch in left.files]
	right_patches = [patch.patch for patch in right.files]
	return left.commit.message == right.commit.message and left_patches == right_patches


def find_commit_equivalent_in_set(left: Commit, pr_commits: Set[Commit]) -> Commit | None:
	for right in pr_commits:
		if cmp_commit(left, right):
			return right
	else:
		return None


def crame(g: Github, pr_id: int, repo_name_or_id: str | int) -> Coal:
	"""
	Return the commits in base (target) branch corresponding to the commit from a PR
	It is useful in case of merge rebase workflow on github because the hash of the
	commits is not the same between the 2 branches.

	Github object argument must already be connected and authenticated

	Raise a github.GithubException.UnknownObjectException if the PR/repo does not exist
	Raise an exception if the PR is not merged
	"""
	repo = g.get_repo(repo_name_or_id)
	pr = repo.get_pull(pr_id)

	if not pr.merged:
		raise Exception("Pr is not merged")

	pr_commits = {commit for commit in pr.get_commits()}
	target_branch = repo.get_branch(pr.base.ref)
	found_commits_in_head = set()
	found_commits_in_target = []

	for commit in repo.get_commits(target_branch.commit.sha):
		maybe_equivalent = find_commit_equivalent_in_set(commit, pr_commits)
		if maybe_equivalent is not None:
			found_commits_in_head.add(maybe_equivalent)
			found_commits_in_target.append(commit)
			continue

	commits_not_found = pr_commits.difference(found_commits_in_head)
	return Coal(
		head_branch_name=pr.head.ref,
		target_branch_name=pr.base.ref,
		commits_in_target=found_commits_in_target,
		commits_not_found=commits_not_found
	)


@click.command()
@click.option("--repo", "-r", required=True, type=str, help="Github repository. Example: 'Baduit/Cramer'")
@click.option("--pr", "-p", required=True, type=int, help="Id of a PR")
@click.option("--hostname", "-h", type=str, help="Hostname,  useful for github entrerprise with custome hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--format-output", "-f", type=click.Choice(["text", "json", "toml"], case_sensitive=False), default="text", help="Format of the output")
def main(repo, pr, hostname, token_path, format_output):
	token = read_token(token_path)
	auth = Auth.Token(token)
	base_url = f"https://{hostname}/api/v3" if hostname else Consts.DEFAULT_BASE_URL

	with Github(auth=auth, base_url=base_url) as g:
		coal = crame(g, pr, repo)
		if format_output == "text":
			print_text(coal)
		elif format_output == "json":
			print_json(coal)
		elif format_output == "toml":
			print_toml(coal)
		else:
			assert False, "It should not be possible to reach here"
