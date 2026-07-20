# Upload Screenshot

<p>Paste a screenshot anywhere on this page (Ctrl+V).</p>

<div
    id="dropzone"
    style="
        border: 2px dashed #999;
        padding: 20px;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: #0f172a;
        border-radius: 8px;
    ">
    No image pasted yet
</div>

<br>

<label for="filename">
    Filename:
</label>

<input
    type="text"
    id="filename"
    placeholder="dashboard-overview">

<br><br>

<button id="generate">
    Generate Markdown
</button>

<button id="copy-markdown">
    Copy Markdown
</button>

<button id="download">
    Download Image
</button>


<button id="submit-issue">
    Create Upload Issue
</button>


<br><br>

<label for="markdown">
    Markdown:
</label>

<textarea
    id="markdown"
    rows="4"
    cols="80"
    readonly>
</textarea>