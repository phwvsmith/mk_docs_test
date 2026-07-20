let imageData = null;

function generateDefaultFilename() {
    const now = new Date();

    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, "0");
    const dd = String(now.getDate()).padStart(2, "0");

    const hh = String(now.getHours()).padStart(2, "0");
    const mi = String(now.getMinutes()).padStart(2, "0");
    const ss = String(now.getSeconds()).padStart(2, "0");

    return `screenshot-${yyyy}${mm}${dd}-${hh}${mi}${ss}`;
}

document.addEventListener("paste", (event) => {

    const items = event.clipboardData.items;

    for (let i = 0; i < items.length; i++) {

        if (items[i].type.startsWith("image/")) {

            const file = items[i].getAsFile();

            const reader = new FileReader();

            reader.onload = (e) => {

                imageData = e.target.result;

                const dropzone = document.getElementById("dropzone");

                dropzone.innerHTML = "";

                const img = document.createElement("img");

                img.src = imageData;
                img.alt = "Screenshot Preview";
                img.style.maxWidth = "100%";
                img.style.maxHeight = "280px";
                img.style.objectFit = "contain";

                dropzone.appendChild(img);

                const filenameInput =
                    document.getElementById("filename");

                if (!filenameInput.value.trim()) {
                    filenameInput.value =
                        generateDefaultFilename();
                }

                document.getElementById("markdown").value =
                    `../../assets/images/${filenameInput.value}.png`;
            };

            reader.readAsDataURL(file);

            break;
        }
    }
});

document.getElementById("generate").addEventListener("click", () => {

    const filename =
        document.getElementById("filename").value.trim();

    if (!filename) {
        alert("Enter a filename");
        return;
    }

    document.getElementById("markdown").value =
        `../../assets/images/${filename}.png`;
});

const copyButton =
    document.getElementById("copy-markdown");

if (copyButton) {

    copyButton.addEventListener("click", async () => {

        const markdown =
            document.getElementById("markdown").value;

        if (!markdown) {
            alert("Generate markdown first");
            return;
        }

        await navigator.clipboard.writeText(markdown);

        copyButton.textContent = "Copied!";

        setTimeout(() => {
            copyButton.textContent = "Copy Markdown";
        }, 2000);
    });

}

const downloadButton =
    document.getElementById("download");

if (downloadButton) {

    downloadButton.addEventListener("click", () => {

        if (!imageData) {
            alert("Paste an image first");
            return;
        }

        const filename =
            document.getElementById("filename").value.trim() ||
            "screenshot";

        const link = document.createElement("a");

        link.href = imageData;
        link.download = `${filename}.png`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

}

const submitIssueButton =
    document.getElementById("submit-issue");

if (submitIssueButton) {

    submitIssueButton.addEventListener("click", () => {

        if (!imageData) {
            alert("Paste an image first");
            return;
        }

        const filename =
            document.getElementById("filename").value.trim();

        if (!filename) {
            alert("Enter a filename");
            return;
        }

        const issueTitle =
            `[UPLOAD] ${filename}`;

        const issueBody =
`Filename: ${filename}.png

IMAGE_DATA
${imageData}
`;

        const url =
            "https://github.com/Public-Health-Wales/ndap_central_doc_repo/issues/new"
            + "?title=" + encodeURIComponent(issueTitle)
            + "&body=" + encodeURIComponent(issueBody);

        window.open(url, "_blank");
    });

}