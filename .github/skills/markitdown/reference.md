# MarkItDown Reference

Quick reference for Microsoft MarkItDown file conversion utility.

## Installation

### Full Installation
```bash
pip install 'markitdown[all]'
```

### Selective Installation
```bash
pip install 'markitdown[pdf]'                    # PDF only
pip install 'markitdown[docx]'                   # Word documents
pip install 'markitdown[pptx]'                   # PowerPoint
pip install 'markitdown[xlsx]'                   # Excel
pip install 'markitdown[audio]'                  # Audio transcription
pip install 'markitdown[image]'                  # Image OCR
pip install 'markitdown[azure-doc-intelligence]' # Azure AI PDF
pip install 'markitdown[llm]'                    # LLM image descriptions
```

## Command-Line Usage

```bash
# Basic conversion
markitdown file.pdf

# Save to file
markitdown file.pdf > output.md
markitdown file.pdf -o output.md

# Batch conversion
for file in *.pdf; do markitdown "$file" > "${file%.pdf}.md"; done
```

## Python API

### Basic Usage
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

### Stream Processing
```python
with open("file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```

### With Azure Document Intelligence
```python
md = MarkItDown(
    azure_doc_intelligence_endpoint="https://your-resource.cognitiveservices.azure.com",
    azure_doc_intelligence_key="your-key"
)
```

### With LLM Image Descriptions
```python
md = MarkItDown(
    llm_model="gpt-4o",  # or gpt-4o-mini
    llm_client=None       # Uses default client
)
```

## Supported Formats

| Format | Extensions | Features |
|--------|-----------|----------|
| **PDF** | .pdf | Text, tables, links, structure |
| **Word** | .docx | Headings, lists, tables, images, links |
| **PowerPoint** | .pptx | Slides, titles, content, images |
| **Excel** | .xlsx, .xls | Sheets, tables, headers |
| **Images** | .png, .jpg, .jpeg, .gif | EXIF, OCR, LLM descriptions |
| **Audio** | .wav, .mp3 | Transcription, timestamps |
| **HTML** | .html | Content, links, tables |
| **CSV** | .csv | Data tables |
| **JSON** | .json | Structure preservation |
| **XML** | .xml | Data extraction |
| **ZIP** | .zip | Archive processing |
| **EPub** | .epub | E-book content |
| **YouTube** | URLs | Metadata, transcripts |

## Docker Usage

```bash
# Build
docker build -t markitdown:latest .

# Run
docker run --rm -i markitdown:latest < input.pdf > output.md

# With volume
docker run --rm -v $(pwd):/data markitdown:latest /data/file.pdf
```

## Common Patterns

### Batch Processing
```python
import os
from markitdown import MarkItDown

md = MarkItDown()

for filename in os.listdir("input/"):
    if filename.endswith(('.pdf', '.docx', '.pptx')):
        result = md.convert(f"input/{filename}")
        base = os.path.splitext(filename)[0]
        with open(f"output/{base}.md", "w") as f:
            f.write(result.text_content)
```

### Error Handling
```python
try:
    result = md.convert("file.pdf")
    markdown = result.text_content
except Exception as e:
    print(f"Conversion failed: {e}")
```

### Memory-Efficient Processing
```python
with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```

## Output Format

MarkItDown produces clean, structured Markdown:

```markdown
# Document Title

## Section Heading

Content with **bold** and *italic* formatting.

- Bullet lists
- Preserved from source

| Table | Headers |
|-------|---------|
| Data  | Values  |

[Links](https://example.com) maintained.

![Images](path/to/image.png) included.
```

## Best Practices

### Performance
- Use streams for files >10MB
- Batch process multiple files
- Cache converted results
- Use selective dependencies

### Quality
- High-resolution images for OCR
- Well-formatted source documents
- Azure Document Intelligence for complex PDFs
- LLM descriptions for important images

### Integration
- Check token counts for LLM limits
- Chunk long documents
- Preserve metadata in context
- Validate output structure

## Troubleshooting

### Common Issues

**Import errors:**
```bash
pip install --upgrade 'markitdown[all]'
```

**Memory errors:**
- Use `convert_stream()` instead of `convert()`
- Process files in smaller batches
- Increase available system memory

**Poor OCR:**
- Increase image resolution
- Improve contrast/brightness
- Use Azure Document Intelligence
- Verify image orientation

**Missing content:**
- Check source file quality
- Try Azure enhancement
- Verify file isn't corrupted
- Use appropriate dependencies

## Requirements

- Python 3.10+
- Virtual environment recommended
- Optional: Azure subscription for enhanced features
- Optional: OpenAI API for image descriptions

## Additional Resources

- [GitHub Repository](https://github.com/microsoft/markitdown)
- [PyPI Package](https://pypi.org/project/markitdown/)
- [Azure Document Intelligence](https://azure.microsoft.com/products/ai-services/ai-document-intelligence)
- [OpenAI API](https://platform.openai.com/)
