from dataclasses import dataclass
from typing import List, Set

from github.Commit import Commit

@dataclass
class Coal:
	head_branch_name: str
	target_branch_name: str
	commits_in_target: Set[Commit]
	commits_not_found: List[Commit]
