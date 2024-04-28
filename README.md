# Cramer
Commit   
Retriever   
After   
MErge   
Rebase   

When using the merge rebase workflow with Github, the sha of the commit between the main branch and the feature branch is not the same. This tool helps to find the commit in the main branch of a PR. (I say main branch but it works with any base branch)

The output can look like this : ![Output example, it show the base and head branch of a PR and the information of the commit found in the base branch](/Example.png)

If you want a more sober output or an easily parsed output you can change it with the `-f` option.

You can also just use the `crame` function in your python code:
```python
def crame(g: Github, pr_id: int, repo_name_or_id: str | int) -> Coal:
"""[...]"""

@dataclass
class Coal:
	head_branch_name: str
	target_branch_name: str
	commits_in_target: Set[Commit]
	commits_not_found: List[Commit]
```

## Tool Usage
```
Usage: crame [OPTIONS]

Options:
  -r, --repo TEXT                 Github repository. Example: 'Baduit/Cramer'
                                  [required]
  -p, --pr INTEGER                Id of a PR  [required]
  -h, --hostname TEXT             Hostname,  useful for github enterprise
                                  with custom hostname
  -t, --token-path TEXT           Path of the file where the token is stored
  -f, --format-output [text|json|toml|rich]
                                  Format of the output
  --help                          Show this message and exit.
```
## Installation
`pip install git+https://github.com/Baduit/Cramer`

(It is not on pypi)