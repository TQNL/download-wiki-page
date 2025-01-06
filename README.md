Below is an example **README** you can include alongside the script. It highlights all the current features, usage instructions, dependencies, and limitations.

I originally made this with the intend of making personal editing of [minecraft wiki](https://minecraft.wiki/) pages easier, but use it for whatever, but keep in mind the limitations.

---

# Wget + HTML-to-Markdown Downloader

A simple **Tkinter**-based Python script that downloads a web page using **`wget`**, renames it to `.html` if no extension is present, and optionally converts it to **Markdown** using the **MarkItDown** Python library. The script also creates a timestamped folder to organize downloaded files.

## Key Features

1. **Automatic Folder Creation**  
   - Creates a subfolder named with the current date and time (e.g., `download_20250106_153045`).  
   - All downloaded and converted files are placed in this folder.

2. **Wget Integration**  
   - Checks for `wget` in the system PATH.  
   - If not found, it attempts to use `wget.exe` in the current working directory (for Windows compatibility).

3. **File Renaming to `.html`**  
   - If the downloaded file has no extension, the script renames it to `.html`.

4. **HTML-to-Markdown Conversion**  
   - If the **MarkItDown** Python library is installed (`pip install markitdown`), the script converts the `.html` file into a `.md` file.  
   - If MarkItDown isn’t installed, it simply skips the conversion step and notifies you via a message box.

5. **Tkinter Graphical User Interface**  
   - Provides a simple GUI with:
     - **Text field** for entering the download URL.  
     - **“Download” button** to initiate the download process.  
     - **Labels** explaining the script’s **Features** and **Limitations** in the same window.

6. **Error Handling**  
   - Handles common errors gracefully, including:
     - Folder creation issues (permissions, filesystem errors).  
     - Missing `wget` executable.  
     - Failures during the download process (e.g., invalid URL, server error).  
     - Problems renaming files or writing Markdown output.

## Requirements

- **Python 3.6+** (the script uses standard libraries like `os`, `shutil`, `subprocess`, and `datetime`).
- **Tkinter** (should be included by default on most systems; on some Linux distros, you may need to install `python3-tk`).
- **wget**:
  - Installed in the system PATH (Linux/macOS) or
  - `wget.exe` in the same folder (Windows).
- **MarkItDown** (optional, for HTML-to-Markdown conversion):
  ```bash
  pip install markitdown
  ```

## Usage

1. **Clone/Download** this script along with the **README** into a folder on your computer.
2. **Open a terminal** (Linux/macOS) or **Command Prompt/PowerShell** (Windows).
3. **Run** the script:
   - On Linux/macOS:
     ```bash
     python3 tkinter_wget_markitdown.py
     ```
   - On Windows:
     ```bash
     python tkinter_wget_markitdown.py
     ```
4. **Enter** the URL you want to download in the **“Enter URL:”** text field.
5. **Click** the **“Download”** button. The script will:
   - Create a timestamped folder (like `download_20250106_153045`).
   - Call `wget` to download the file into that folder.
   - If the file has no extension, rename it to `.html`.
   - Attempt to convert it to `.md` if `MarkItDown` is installed.
   - Display a success or error message.

## Example

1. Enter a URL such as `https://minecraft.wiki/w/Advancement_definition`.
2. Click **Download**.
3. The script creates a folder named **`download_20250106_153045`**.
4. If the URL ends with a slash (no specific file), the resulting file will be named **`index.html`**.
5. If MarkItDown is installed, you will see **`index.md`** in the same folder after conversion.

## Limitations

1. **Single-File Only**  
   - The script doesn’t automatically fetch additional resources (CSS, images, etc.).  
2. **Basic Wget Usage**  
   - Advanced features (recursion, authentication, cookies, etc.) are not exposed.  
3. **No MIME Detection**  
   - Files with no extension default to `.html`, which may mislabel non-HTML content.  
4. **Overwrites**  
   - Existing files with the same names can be overwritten without warning.  
5. **No Progress Indicators**  
   - No real-time feedback on download progress.  
6. **MarkItDown Conversion**  
   - More complex HTML might not convert perfectly, and special content (scripts, iframes) could be lost.

## Stuff
- Feel free to **fork** this script, I don't do maintainers, nor pull requests.
- Disclaimer: this was originally developed for personal use, created using AI assistance, and licensed under the GPL-3.0 license.
- **Enjoy downloading your content and converting it to Markdown with a single click!**
