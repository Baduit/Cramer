from .coal import Coal

def print_text(result: Coal):
	if result.commits_not_found:
		print(f"The following commits were not found in branch {result.target_branch_name}: {result.commits_not_found}")
	print(f"The following commits were foundin branch {result.target_branch_name}: {result.commits_in_target}")


def print_json(result: Coal):
	pass


def print_toml(result: Coal):
	pass