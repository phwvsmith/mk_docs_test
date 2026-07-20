# How to Edit & Add A Page: Data Engineers

Welcome! This guide helps you get set up and start working with the NDAP Documentation platform.

---

## 👥 Who is this for?

- Data Engineers
- Developers working with data pipelines or datasets

---

## 🎯 What you’ll achieve

By the end of this guide, you will:

- Have access to the documentation repository
- Be able to run docs locally
- Understand how to contribute changes
- Know where to go next

---

## ⚙️ Step 1: Set up your environment

### ✅ Open VS Code in WSL

1. Open VS Code  
2. select clone git repository

### ✅ If not using WSL, open VS Code

1. Launch VS Code by double-clicking the desktop icon or searching for it in the Start Menu
2. Open the integrated terminal via **Terminal** in the top menu bar, then **New Terminal**
3. Ensure the terminal type is set to **Command Prompt** - click the dropdown arrow next to the `+` in the terminal panel if it defaults to PowerShell

### ✅ Clone the repository

```bash
git clone git@github.com:Public-Health-Wales/ndap_central_doc_repo.git
cd ndap_central_doc_repo
```

### ✅ Create Virtual Environment

**WSL:**
```bash
python3 -m venv .venv
```

**Windows CMD:**
```cmd
python -m venv .venv
```

### ✅ Activate the Environment

**WSL:**
```bash
source .venv/bin/activate
```

**Windows CMD:**
```cmd
.venv\Scripts\activate
```

### ✅ Check if pip is working

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### ✅ Install dependencies

```bash
python -m pip install -r requirements.txt
```

### ✅ Check if local site is working

**WSL:**
```bash
mkdocs serve
```

**Windows CMD:**
```cmd
python -m mkdocs serve
```

Then open your browser at: `http://127.0.0.1:8000`

## ⚙️ Step 2: Make your changes
### ✅ Create new branch

```bash
git checkout -b feature/your-branch-name
```

> ⚠️ Branch names cannot contain spaces, use hyphens.

### ✅ Edit Documents

Every folder must have this structure:
1. `.pages` - all markdown pages must be listed here under the `nav` block
2. `index.md` - must be present. This is the landing page. Write an overview or anything else appropriate for your team's landing page.
3. any other `file.md` as needed
4. all files except `.pages` must be `.md` format
    
### ✅ Commit and push to git

```bash
git add .
git commit -m "Update documentation"
git push origin feature/your-branch-name
```

### ✅ Merge to Main

1. Raise PR to Main
2. Merge PR to main
3. Once merged, GH Actions will trigger two pipelines
4. Wait until the "Pages build and deployment" workflow is complete

### ✅ Check the updated site

Navigate to: https://Public-Health-Wales.github.io/ndap_central_doc_repo/

### ✅ Troubleshooting

1. Please do not touch any other file apart from your team's folder
2. Check if your files are correctly listed under the `nav` section in the `.pages` file in your folder
3. Check if the local site is working before pushing to the live site
4. If nothing is working, please reach out to the DE team
5. pip not working:
```bash
python -m ensurepip --upgrade
```
6. mkdocs not found:
```bash
python -m pip install -r requirements.txt
```
7. site not updating: check if the PR is merged and the Pages build & deployment Actions workflow is complete
8. navigation issues: check if your `.md` files are listed under the `nav` section of the `.pages` file

