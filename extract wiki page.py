#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import shutil
import os
import datetime
from urllib.parse import urlparse

# Attempt to import MarkItDown. If not installed, we'll set a flag.
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False

FEATURES_TEXT = (
    "Key Features:\n"
    "1. Creates a subfolder named with the current date and time.\n"
    "2. Checks for wget in system PATH or the current folder.\n"
    "3. Renames downloaded files to .html if no extension is present.\n"
    "4. Converts HTML file to Markdown (if MarkItDown is installed).\n"
    "5. Provides concise error handling for common failures.\n"
)

LIMITATIONS_TEXT = (
    "Key Limitations:\n"
    "1. Single-File Only: Only downloads one file per URL (no related resources).\n"
    "2. Basic Wget Usage: No advanced features like recursion, cookies, etc.\n"
    "3. File Overwrites: Overwrites existing files without warning.\n"
    "4. No MIME Detection: Defaults to .html if no extension, which may mislabel.\n"
    "5. MarkItDown Limitations: Complex HTML may not convert perfectly.\n"
    "6. No Progress Indicators: Large file downloads show no progress.\n"
    "7. Requires Wget & Permissions: Wget in PATH or local folder; write permission required.\n"
    "8. Basic Error Handling: Partial downloads or complex redirects aren’t handled in-depth.\n"
)

def convert_file_to_markdown(input_file_path, output_file_path):
    """
    Convert an HTML file to Markdown using the MarkItDown Python library.
    Raises a RuntimeError on failure.
    """
    try:
        md = MarkItDown()
        result = md.convert(input_file_path)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(result.text_content)
    except Exception as e:
        raise RuntimeError(f"Error converting HTML to Markdown: {e}")

def download_file():
    """
    Main download and conversion workflow:
      1) Create a timestamped folder
      2) Locate wget or wget.exe
      3) Download the file
      4) Rename if no extension -> .html
      5) Convert to Markdown if MarkItDown is installed
      6) Show success/error messages
    """
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Required", "Please enter a URL.")
        return

    # 1. Create a timestamped folder (e.g., 'download_20250106_153045')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"download_{timestamp}"
    try:
        os.makedirs(folder_name, exist_ok=True)
    except OSError as e:
        messagebox.showerror("Folder Error", f"Could not create folder '{folder_name}':\n{e}")
        return

    # 2. Locate wget
    wget_path = shutil.which("wget")
    if wget_path is None:
        # If not in PATH, check for wget.exe locally (primarily for Windows)
        local_wget = os.path.join(os.getcwd(), "wget.exe")
        if os.path.exists(local_wget):
            wget_path = local_wget
        else:
            messagebox.showerror(
                "wget Not Found",
                "Could not find 'wget' in PATH or 'wget.exe' in the current folder."
            )
            return

    # 3. Determine an output filename based on the URL
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or "index"

    # Construct the download path in our new folder
    download_path = os.path.join(folder_name, filename)

    # Attempt to download using wget
    try:
        subprocess.run([wget_path, "-O", download_path, url], check=True)
    except FileNotFoundError:
        messagebox.showerror("Missing Executable", "Could not run wget. Ensure it is installed or in the folder.")
        return
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Download Error", f"An error occurred while downloading:\n{e}")
        return
    except Exception as e:
        messagebox.showerror("Unknown Error", f"An unexpected error occurred:\n{e}")
        return

    # 4. Rename to .html if there's no extension
    root_name, ext = os.path.splitext(download_path)
    if not ext:
        new_download_path = root_name + ".html"
        try:
            if os.path.exists(new_download_path):
                os.remove(new_download_path)  # Overwrite (simple approach)
            os.rename(download_path, new_download_path)
            final_html_path = new_download_path
        except OSError as e:
            messagebox.showerror("Rename Error", f"Could not rename file:\n{e}")
            return
    else:
        final_html_path = download_path

    # 5. Convert to Markdown if MarkItDown is available
    final_markdown_path = None
    if MARKITDOWN_AVAILABLE:
        final_markdown_path = os.path.splitext(final_html_path)[0] + ".md"
        try:
            convert_file_to_markdown(final_html_path, final_markdown_path)
        except RuntimeError as e:
            messagebox.showerror("Conversion Error", str(e))
            return
        except OSError as e:
            messagebox.showerror("File Error", f"Could not create or write to Markdown file:\n{e}")
            return
        except Exception as e:
            messagebox.showerror("Unknown Conversion Error", f"An unexpected error occurred:\n{e}")
            return
    else:
        messagebox.showwarning(
            "MarkItDown Not Installed",
            "The Python 'markitdown' library is not installed. Skipping HTML-to-Markdown conversion."
        )

    # 6. Show success message
    if final_markdown_path and os.path.exists(final_markdown_path):
        messagebox.showinfo(
            "Success",
            f"Downloaded to:\n{final_html_path}\n\n"
            f"Converted to:\n{final_markdown_path}\n\n"
            f"All files are in the folder:\n{folder_name}"
        )
    else:
        messagebox.showinfo(
            "Success",
            f"Successfully downloaded:\n{final_html_path}\n\n"
            f"All files are in the folder:\n{folder_name}\n"
            f"(No Markdown file created.)"
        )

def main():
    global url_entry

    # Create the main application window
    root = tk.Tk()
    root.title("Wget + HTML-to-Markdown Downloader")

    # Frame for input/labels
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, padx=10, pady=10)

    # URL label and entry
    tk.Label(main_frame, text="Enter URL:").grid(row=0, column=0, sticky="e")
    url_entry = tk.Entry(main_frame, width=50)
    url_entry.grid(row=0, column=1, padx=5)

    # Download button
    tk.Button(main_frame, text="Download", command=download_file).grid(row=0, column=2, padx=5)

    # Features box
    features_label = tk.Label(main_frame, text=FEATURES_TEXT, justify="left", fg="blue")
    features_label.grid(row=1, column=0, columnspan=3, pady=(10, 5), sticky="w")

    # Limitations box
    limitations_label = tk.Label(main_frame, text=LIMITATIONS_TEXT, justify="left", fg="red")
    limitations_label.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky="w")

    # Start Tkinter loop
    root.mainloop()

if __name__ == "__main__":
    main()
