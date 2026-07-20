# Common Issues & Troubleshooting

If something didn’t work as expected after you edited a page, you’ll likely find the answer here.

---

## My changes didn’t appear on the website

**What’s happening**
After you click **Commit changes**, your update goes through an automated process:
- A draft change is created
- The system checks it
- It is merged and published automatically

**What to do**
- Wait 2-3 minutes and refresh the page
- Try a hard refresh (Ctrl + Shift + R)

---

## I committed changes but nothing seems to happen

**What’s happening**
Your change is being processed in the background. In some cases:
- The system may be validating your update
- The change may still be merging

**What to do**
- Check the **Pull Requests** tab in GitHub (optional)
- Wait till the PR status is **Merged**
- Wait 2-3 minutes and refresh the page

---

## My changes didn’t get published

**What’s happening**
Sometimes your change cannot be applied automatically. This usually happens when:
- Someone else edited the same page at the same time
- The system could not safely combine both updates
- Your change broke something e.g. it has links to invalid pages etc.

**What to do**
- Open your Pull Request (a link is shown after you commit)
- You may see a message about a **conflict**
- Re-apply your change based on the latest version of the page
- You may see a message about **validation failure**
- click on the red validation failure.
- It will show you what failed
- Close the PR, and correct it and re-commit.

👉 If unsure, contact the support team

---

## What is a “merge conflict”?

A merge conflict happens when:
- Two people edit the same part of a page at the same time
- The system cannot decide which version to keep

**Example (simplified)**

Two users edit the same sentence differently:

- Person A: updates step instructions  
- Person B: rewrites the same section  

The system cannot automatically combine them.

---

**What the system does**
- It tries to automatically combine changes (most of the time this works ✅)
- If not, it pauses and asks for manual resolution

---

**What you should do**
- Open your edit again
- Copy your changes
- Apply them to the latest version of the page

---

## My formatting looks wrong

**Common causes**
- Missing blank lines
- Incorrect heading format
- Improper list indentation

**What to do**
- Check the [Formatting Guide](formatting-guideline.md)
- Use simple Markdown formatting
- Preview changes before committing

---

## My image is not showing

**Common causes**
- Incorrect file path
- Image not uploaded to the repository
- File name mismatch (case-sensitive)

**What to do**
- Confirm the image is uploaded
- Check the file path
- See the [Images and Files Guide](images-and-files.md)

---

## Good to know

- You don’t need Git or coding knowledge  
- Most changes are published automatically within seconds  
- If something fails, it’s usually due to overlapping edits  

---

## ❓ Still stuck?

If your issue isn’t listed here:

👉 Check the [FAQ](FAQ.md)
👉 Or go to [Who to Contact](Who-to-contact.md)
