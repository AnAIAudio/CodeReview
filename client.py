import os
import argparse

from github import Github, Auth

from prompt import system_prompt
from local_llm import translate_local_llm


def get_pr_diff(token, repo_name, pr_number):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    diff_content = []
    for file in files:
        diff_content.append(f"File: {file.filename}\n")
        diff_content.append(f"Status: {file.status}\n")
        diff_content.append(f"Additions: {file.additions}\n")
        diff_content.append(f"Deletions: {file.deletions}\n")
        diff_content.append(f"Changes: {file.changes}\n")
        diff_content.append(f"Patch:\n{file.patch}\n")
        diff_content.append("-" * 40 + "\n")

    return "\n".join(diff_content)


def review_code(diff):
    user_prompt = f"{system_prompt}\n다음 코드 변경사항을 리뷰해주세요:\n\n{diff}"
    response = translate_local_llm(os.environ["LOCAL_AI_KEY"], user_prompt)
    return response


def post_review(token, repo, pr_number, review):
    g = Github(token)
    repo = g.get_repo(repo)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(review)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--github_token", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--pull_request_number", required=True, type=int)
    args = parser.parse_args()

    diff = get_pr_diff(args.github_token, args.repository, args.pull_request_number)
    print(f"diff : \n{diff}")
    review = review_code(diff)
    print(f"review: \n{review}")
    post_review(args.github_token, args.repository, args.pull_request_number, review)


if __name__ == "__main__":
    main()
