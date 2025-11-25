import logging
import re
import sys
from typing import Dict, Optional

from environs import Env
from github.PullRequest import PullRequest

env = Env()

TASK_QUEUE = env("INPUT_TASK_QUEUE")
TASK_KEY_PATTERN = re.compile(rf"{re.escape(TASK_QUEUE)}-\d+")  # noqa
logger = logging.getLogger(__name__)


def get_pr_commits(
    *,
    pr: PullRequest,
) -> list[str]:
    """
    Get all commits from PR to a list if there are many, or str if there is one.
    Args:
      pr: GitHub PullRequest object.
    Returns:
      List of all current PR's commits.
    """
    commits = []

    for commit in pr.get_commits():
        all_matches = TASK_KEY_PATTERN.findall(commit.commit.message)
        if not all_matches:
            continue

        commits.extend(all_matches)

    return commits


def check_if_pr(*, data: dict[str, str]):
    """
    Checking the pull_request key in action.
    Args:
      data: dict with available data from runner.
    Raises:
      System error exit code 1.
    """
    try:
        data["pull_request"]
    except KeyError:
        logger.warning("[SKIPPING] You can use this action only on Pull Request")
        sys.exit(1)
