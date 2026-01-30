import tkinter as tk
from tkinter import messagebox
import re
from github import Github, GithubException
import threading


class GitHubTagger(tk.Tk):
    """
    존@나 간단한 깃@허브 태그 프로그램
    """

    def __init__(self):
        super().__init__()
        self.title("깃@허브 태거")
        self.geometry("500x380")

        # --- Input Fields ---
        tk.Label(self, text="토@큰:").pack(pady=(10, 0))
        self.token_var = tk.StringVar()
        tk.Entry(self, textvariable=self.token_var, show="*").pack(fill=tk.X, padx=10)

        tk.Label(self, text="리@포 주@소:").pack(pady=(10, 0))
        self.url_var = tk.StringVar()
        tk.Entry(self, textvariable=self.url_var).pack(fill=tk.X, padx=10)

        tk.Label(self, text="태@그 이름:").pack(pady=(10, 0))
        self.tag_name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.tag_name_var).pack(fill=tk.X, padx=10)

        tk.Label(self, text="태@그 매@세지:").pack(pady=(10, 0))
        self.tag_message_var = tk.StringVar()
        tk.Entry(self, textvariable=self.tag_message_var).pack(fill=tk.X, padx=10)

        tk.Label(self, text="커@밋 SHA (필@수 아님):").pack(pady=(10, 0))
        self.commit_sha_var = tk.StringVar()
        tk.Entry(self, textvariable=self.commit_sha_var).pack(fill=tk.X, padx=10)

        # --- Action Button ---
        self.create_button = tk.Button(self, text="태@그 만@들기", command=self.start_tag_creation_thread)
        self.create_button.pack(pady=20)

        # --- Status Label ---
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self, textvariable=self.status_var)
        self.status_label.pack()
        self.update_status("준@비.", "blue")

    def start_tag_creation_thread(self):
        """
        Starts the tag creation process in a separate thread to keep the GUI responsive.
        """
        self.create_button.config(state=tk.DISABLED)
        self.status_var.set("하@는중")
        self.status_label.config(fg="orange")
        
        thread = threading.Thread(target=self.create_tag)
        thread.daemon = True  # Allows main window to exit even if thread is running
        thread.start()

    def create_tag(self):
        """
        Handles the logic of creating a GitHub tag.
        This method is run in a separate thread. -> 뭐라하는지 모르겠음
        """
        token = self.token_var.get()
        repo_url = self.url_var.get()
        tag_name = self.tag_name_var.get()
        tag_message = self.tag_message_var.get()
        commit_sha = self.commit_sha_var.get().strip()

        if not all([token, repo_url, tag_name, tag_message]):
            self.after(0, lambda: messagebox.showerror("오고@곡", "필@수 문구를 채@워주세요"))
            self.after(0, lambda: self.update_status("오고@곡 필드 미@싱", "red"))
            return

        match = re.search(r"github\.com/([^/]+/[^/]+)", repo_url)
        if not match:
            self.after(0, lambda: messagebox.showerror("오고@곡", "잘못된 깃@허브 URL 형식입니다"))
            self.after(0, lambda: self.update_status("오고@곡 잘못된 URL", "red"))
            return
        repo_path = match.group(1).replace('.git', '')

        try:
            g = Github(token)
            repo = g.get_repo(repo_path)

            if not commit_sha:
                self.after(0, lambda: self.status_var.set(f"'{repo.default_branch}'에서 최@신 커@밋 가@져오는 중..."))
                default_branch = repo.get_branch(repo.default_branch)
                commit_sha = default_branch.commit.sha
                self.after(0, lambda: self.commit_sha_var.set(commit_sha))

            self.after(0, lambda: self.status_var.set(f"커@밋 {commit_sha[:7]}에 태@그 '{tag_name}' 생@성 중..."))

            # Create an annotated tag object first
            tag_object = repo.create_git_tag(
                tag=tag_name,
                message=tag_message,
                object=commit_sha,
                type='commit'
            )
            # Then, create a reference (the actual tag) pointing to the tag object
            repo.create_git_ref(ref=f"refs/tags/{tag_name}", sha=tag_object.sha)

            self.after(0, lambda: messagebox.showinfo("성@공", f"태@그 '{tag_name}' 성@공적으로 '{repo_path}'에 생@성되었습니다!"))
            self.after(0, lambda: self.update_status(f"성@공! 태@그 '{tag_name}' 생@성됨.", "green"))

        except GithubException as e:
            error_message = f"깃@허브 API 오고@곡 ({e.status}): {e.data.get('message', '알 수 없는 오고@곡')}"
            self.after(0, lambda: messagebox.showerror("깃@허브 오고@곡", error_message))
            self.after(0, lambda: self.update_status(f"실@패: {e.data.get('message', '')}", "red"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("오고@곡", f"예@상치 못한 오고@곡가 발@생했습니다: {e}"))
            self.after(0, lambda: self.update_status(f"실@패: {e}", "red"))

    def update_status(self, message, color):
        self.status_var.set(message)
        self.status_label.config(fg=color)
        self.create_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = GitHubTagger()
    app.mainloop()