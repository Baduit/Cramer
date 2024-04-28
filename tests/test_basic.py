import cramer

from github import Github

def test_basic_success():
	with Github() as g:
		coal = cramer.crame(g, 2, "Baduit/Cramer")
		assert len(coal.commits_in_target) == 1
		assert coal.commits_in_target[0].sha == "52dd8a5d18954c241089e6ac7aabcc6ddc851258"
		assert not coal.commits_not_found
		assert coal.head_branch_name == "feature_for_pr_for_tests"
		assert coal.target_branch_name == "for_pr_tests"
