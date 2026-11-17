# Project status

## Pending public deployment

Phase 3's public URL check is blocked because this project has no GitHub remote. `git remote -v` returned no remotes before and after local repository initialization. The workflow packages the `web/` directory with the RoBERTa-generated report and CSV.

1. Create a public GitHub repository for the project.
2. Add its remote with `git remote add origin <repository-url>`.
3. In the repository, open **Settings → Pages** and set **Source** to **GitHub Actions**.
4. Push `main` with `git push -u origin main`. If Pages was enabled after the push, run **Publish feedback report** from **Actions**.
5. Open the Pages URL returned by the workflow. Check the 80-review summary, filters and CSV download, then add the repository and Pages links to the README and the demo slide.

[GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
