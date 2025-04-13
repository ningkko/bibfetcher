# 🧠 Reference Crawler and BibTeX Generator

This Python script automates the process of retrieving BibTeX entries from article titles using the CrossRef API. It generates a clean `.bib` file that can be directly used in LaTeX or imported into Zotero for streamlined reference management.

---

## 🔍 Purpose

- Fetch BibTeX citations from article titles.
- Standardize BibTeX keys to ensure uniqueness.
- Export results in a structured `.csv` and `.bib` format.
- Facilitate quick bibliography creation via LaTeX or Zotero.

---

## 📥 Input

- `titles.txt`: A plain text file containing one article title per line.

Example:
```
Deep learning for healthcare
A survey on neural networks
```

---

## ⚙️ What It Does

1. **Queries CrossRef API** for each article title.
2. **Extracts DOIs** and downloads BibTeX entries.
3. **Cleans and standardizes** BibTeX keys using first author's last name + year.
4. **Outputs:**
   - `output.csv`: Summary of title, BibTeX, and whether it was found.
   - `citation.bib`: Clean BibTeX file ready for use.

---

## 📤 Output Files

- `output.csv`: Contains three columns — Title, BibTeX Entry, and Found Status.
- `citation.bib`: Cleaned BibTeX entries with unique keys.

---

## 🧪 LaTeX Integration (Optional)

To generate a bibliography using LaTeX:

```latex
\usepackage[
  backend=biber,
  style=vancouver,
  sorting=ynt
]{biblatex}

\addbibresource{citation.bib}

\nocite{*}
\printbibliography
```

Compile with:
```bash
pdflatex yourfile.tex
biber yourfile
pdflatex yourfile.tex
```

---

## 📚 Import to Zotero

To use these citations in **Zotero**:

1. Open Zotero.
2. Go to `File` > `Import...`.
3. Select `citation.bib` as the source file.
4. Choose **BibTeX** format when prompted.
5. The references will be added to your Zotero library.

---

## 🛠️ Requirements

- Python 3.x
- `requests`, `tqdm`

Install dependencies (if needed):
```bash
pip install requests tqdm
```

---

## 🧾 License

MIT License. Free to use and modify.

