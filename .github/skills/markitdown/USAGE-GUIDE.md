# MarkItDown - Complete Usage Guide

Comprehensive guide to using the MarkItDown skill with Claude Code for converting files to Markdown, OCR, transcription, and LLM preprocessing.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Supported Formats](#supported-formats)
- [Complete Use Cases](#complete-use-cases)
- [Advanced Features](#advanced-features)
- [Performance Optimization](#performance-optimization)
- [Best Practices](#best-practices)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `convert to markdown`, `markitdown`, `markdown conversion`
- `extract text`, `get text from`, `read file`
- `OCR`, `optical character recognition`, `text from image`
- `transcribe`, `audio to text`, `speech to text`
- `PDF to markdown`, `Word to markdown`, `file conversion`
- `process document`, `parse file`, `LLM preprocessing`

### Explicit Requests

Be clear about what file type you're converting:

```
✅ GOOD: "Convert this PDF to Markdown"
✅ GOOD: "Extract text from these Word documents"
✅ GOOD: "Transcribe this audio file to text"
✅ GOOD: "Use OCR to get text from this scanned image"
✅ GOOD: "Process all documents in this folder to Markdown"

⚠️ VAGUE: "Convert my files"
⚠️ VAGUE: "Get the text"
```

### Example Invocation Patterns

```bash
# Single file conversion
"Convert report.pdf to Markdown"
"Extract text from presentation.pptx"
"Transcribe meeting-recording.wav to text"

# Batch processing
"Convert all PDFs in the /documents folder to Markdown"
"Process all Word docs and save as .md files"
"Transcribe all audio files in /meetings"

# Advanced features
"Convert this PDF using Azure Document Intelligence"
"Extract text from image with OCR"
"Generate descriptions for images in this PowerPoint"
```

---

## Supported Formats

### Documents

| Format | Extensions | Features |
|--------|-----------|----------|
| **PDF** | .pdf | Text, tables, links, structure |
| **Word** | .docx | Headings, lists, tables, images, links |
| **PowerPoint** | .pptx | Slides, titles, content, images |
| **Excel** | .xlsx, .xls | Sheets, tables, headers |

### Media

| Format | Extensions | Features |
|--------|-----------|----------|
| **Images** | .png, .jpg, .jpeg, .gif | EXIF metadata, OCR, LLM descriptions |
| **Audio** | .wav, .mp3 | Transcription, timestamps |

### Web & Data

| Format | Extensions | Features |
|--------|-----------|----------|
| **HTML** | .html | Content extraction, links, tables |
| **CSV** | .csv | Data tables with formatting |
| **JSON** | .json | Structure preservation |
| **XML** | .xml | Data extraction |

### Archives & E-books

| Format | Extensions | Features |
|--------|-----------|----------|
| **ZIP** | .zip | Archive processing, recursive conversion |
| **EPub** | .epub | E-book content with structure |

### Special

| Format | Type | Features |
|--------|------|----------|
| **YouTube** | URLs | Video metadata, transcripts |

---

## Complete Use Cases

### Use Case 1: Document Processing for LLM Analysis

**Scenario**: Convert research papers to Markdown for AI analysis

**Step-by-step workflow**:

1. **Single document conversion**:
```
Request: "Convert research-paper.pdf to Markdown"

Claude processes:
✓ PDF loaded (45 pages, 8.2 MB)
✓ Text extracted
✓ Tables preserved
✓ Links maintained
✓ Structure converted

Output: research-paper.md (42 KB)
```

**Result**:
```markdown
# Deep Learning for Natural Language Processing

## Abstract

This paper presents a novel approach to neural machine translation...

## 1. Introduction

Recent advances in deep learning have shown significant improvements...

### 1.1 Background

Neural networks have become the dominant architecture...

## 2. Related Work

Previous research by [Author et al., 2023](https://example.com)...

| Model | BLEU Score | Parameters |
|-------|-----------|------------|
| Transformer | 34.5 | 213M |
| Our Model | 38.2 | 189M |

## 3. Methodology

We propose a multi-headed attention mechanism...
```

2. **Batch processing**:
```
Request: "Convert all PDF research papers in /papers/ to Markdown"

Claude processes:
Processing 23 PDFs...
✓ paper-001.pdf → paper-001.md (38 KB)
✓ paper-002.pdf → paper-002.md (51 KB)
✓ paper-003.pdf → paper-003.md (29 KB)
...
✓ paper-023.pdf → paper-023.md (44 KB)

Total: 23 files processed
Success: 23 (100%)
Output directory: /papers/markdown/
```

3. **Analyze with LLM**:
```
Request: "Now analyze all converted papers and summarize key findings"

Claude reads Markdown files and provides:
Summary of 23 Research Papers
==============================

Key Themes:
1. Transformer architectures (15 papers)
2. Few-shot learning (8 papers)
3. Multimodal models (6 papers)

Novel Contributions:
- Paper 7: Efficient attention mechanism (40% faster)
- Paper 12: Zero-shot cross-lingual transfer
- Paper 19: Interpretability framework

Datasets Used:
- GLUE benchmark: 12 papers
- SQuAD: 8 papers
- Custom datasets: 11 papers
...
```

**Expected outcome**:
- Documents converted to LLM-friendly format
- Preserved structure and formatting
- Ready for AI analysis
- Batch processing complete

---

### Use Case 2: OCR for Scanned Documents

**Scenario**: Extract text from scanned document images

**Step-by-step workflow**:

1. **Basic OCR**:
```
Request: "Extract text from scanned-invoice.png using OCR"

Claude processes:
✓ Image loaded (2400x3200 px)
✓ OCR applied
✓ Text extracted
✓ EXIF metadata included
```

**Output**:
```markdown
# Image Metadata
- File: scanned-invoice.png
- Format: PNG
- Size: 2400x3200 pixels
- Camera: Canon EOS R5
- Date: 2024-12-15 10:34:22

# Extracted Text

INVOICE #12345

Bill To:
Acme Corporation
123 Business St
New York, NY 10001

Date: December 15, 2024
Due Date: January 14, 2025

Description                Quantity    Price       Total
---------------------------------------------------------
Professional Services      40 hrs      $150/hr     $6,000
Software License          1           $500        $500
Support Package           1           $200        $200
---------------------------------------------------------
                                       Subtotal:   $6,700
                                       Tax (8%):   $536
                                       Total:      $7,236
```

2. **Enhanced OCR with Azure**:
```
Request: "Use Azure Document Intelligence to extract text from complex-table.png"

Claude processes with Azure AI:
✓ Image uploaded to Azure
✓ Document Intelligence analysis
✓ Table structure detected
✓ Text and layout extracted
✓ Confidence scores calculated
```

**Output**:
```markdown
# Document Analysis (Confidence: 98.5%)

## Table Extracted

| Product Code | Description | Q1 2024 | Q2 2024 | Q3 2024 | Total |
|--------------|-------------|---------|---------|---------|-------|
| PROD-001 | Widget A | $42,500 | $45,230 | $48,120 | $135,850 |
| PROD-002 | Widget B | $38,920 | $41,340 | $39,850 | $120,110 |
| PROD-003 | Widget C | $51,230 | $55,120 | $58,940 | $165,290 |

## Notes Section

Review indicates strong Q3 performance across all products.
Widget C showing exceptional growth trajectory (+14% QoQ).
```

**Expected outcome**:
- Text extracted from images
- Tables preserved
- High accuracy OCR
- Azure AI enhancements

---

### Use Case 3: Audio Transcription

**Scenario**: Transcribe meeting recordings to searchable text

**Step-by-step workflow**:

1. **Single file transcription**:
```
Request: "Transcribe team-meeting-2024-12-15.wav to text"

Claude processes:
✓ Audio loaded (45 minutes, 128 MB)
✓ Speech-to-text processing
✓ Speaker detection (3 speakers)
✓ Timestamps generated
```

**Output**:
```markdown
# Team Meeting Transcription
Date: December 15, 2024
Duration: 45:23
Speakers: 3

## Transcript

[00:00:12] Speaker 1: Good morning everyone. Let's start with the project status update.

[00:00:18] Speaker 2: Thanks. The backend API is now complete. We finished all endpoints yesterday and they're deployed to staging.

[00:00:35] Speaker 3: That's great progress. What about the frontend integration?

[00:00:42] Speaker 2: Frontend team has started integration. They estimate completion by end of week.

[00:01:05] Speaker 1: Excellent. Let's move to the next topic - the database migration.

[00:01:12] Speaker 3: The migration script is ready. We've tested it in dev and staging environments. Both went smoothly.

[00:01:28] Speaker 1: When are we planning production migration?

[00:01:32] Speaker 3: This Saturday at 2 AM. We expect 2-3 hour downtime window.

...

[45:05] Speaker 1: Thanks everyone. Let's reconvene next Monday same time.

[45:12] All: [Agreement sounds]

## Action Items

1. Frontend team: Complete API integration by Friday
2. Speaker 3: Execute production migration Saturday 2 AM
3. All: Review documentation updates by Monday meeting

## Key Decisions

- Approved Saturday maintenance window
- Postponed feature X to next sprint
- Increased testing coverage requirement to 85%
```

2. **Batch transcription**:
```
Request: "Transcribe all WAV files in /meetings/december/ folder"

Claude processes:
Processing 8 audio files...
✓ meeting-2024-12-01.wav (32:15) → transcript
✓ meeting-2024-12-05.wav (48:42) → transcript
✓ meeting-2024-12-08.wav (29:51) → transcript
✓ meeting-2024-12-12.wav (55:13) → transcript
✓ meeting-2024-12-15.wav (45:23) → transcript
✓ meeting-2024-12-18.wav (38:47) → transcript
✓ standup-2024-12-20.wav (15:32) → transcript
✓ planning-2024-12-22.wav (62:18) → transcript

Total: 8 files (4 hours 48 minutes audio)
Output: /meetings/december/transcripts/
```

**Expected outcome**:
- Searchable meeting transcripts
- Speaker identification
- Timestamps for navigation
- Action items extracted
- Batch processing complete

---

### Use Case 4: Office Document Conversion

**Scenario**: Convert Office presentations and spreadsheets

**Step-by-step workflow**:

1. **PowerPoint to Markdown**:
```
Request: "Convert quarterly-review.pptx to Markdown"

Claude processes:
✓ PowerPoint loaded (24 slides)
✓ Slide content extracted
✓ Images processed
✓ Speaker notes included
```

**Output**:
```markdown
# Q4 2024 Quarterly Review

## Slide 1: Title Slide

**Q4 2024 Business Review**
Company Name
December 18, 2024

---

## Slide 2: Executive Summary

### Key Highlights

- Revenue: $4.2M (+12% YoY)
- New Customers: 234
- Customer Retention: 94%
- Team Growth: 8 new hires

![Revenue Chart](images/revenue-chart.png)

*Speaker Notes: Emphasize the strong customer retention rate as a key differentiator*

---

## Slide 3: Revenue Breakdown

| Category | Q4 2024 | Q3 2024 | Growth |
|----------|---------|---------|--------|
| Products | $2.8M | $2.5M | +12% |
| Services | $1.4M | $1.2M | +17% |
| **Total** | **$4.2M** | **$3.7M** | **+14%** |

---

## Slide 4: Customer Acquisition

New customer growth accelerated in November...

![Customer Growth](images/customer-growth.png)

...
```

2. **Excel to Markdown**:
```
Request: "Convert sales-data-2024.xlsx to Markdown"

Claude processes:
✓ Excel workbook loaded (5 sheets)
✓ Data extracted from all sheets
✓ Formulas evaluated
✓ Formatting preserved
```

**Output**:
```markdown
# Sales Data 2024

## Sheet: Monthly Sales

| Month | Revenue | Orders | Avg Order | Growth |
|-------|---------|--------|-----------|--------|
| Jan | $284,592 | 1,234 | $230.65 | - |
| Feb | $301,445 | 1,298 | $232.20 | +5.9% |
| Mar | $318,207 | 1,367 | $232.75 | +5.6% |
| Apr | $295,883 | 1,289 | $229.56 | -7.0% |
| May | $342,109 | 1,456 | $235.02 | +15.6% |
| Jun | $359,421 | 1,523 | $236.02 | +5.1% |

## Sheet: Top Products

| Rank | Product | Units | Revenue |
|------|---------|-------|---------|
| 1 | Laptop Pro 15 | 2,847 | $3,987,580 |
| 2 | Monitor 27" | 1,893 | $1,231,950 |
| 3 | Keyboard Mech | 3,124 | $467,460 |

## Sheet: Sales by Region

...
```

**Expected outcome**:
- Presentations converted to readable format
- Spreadsheet data preserved in tables
- Multiple sheets handled
- Ready for documentation or analysis

---

### Use Case 5: Batch Document Processing Pipeline

**Scenario**: Process entire document library for knowledge base

**Step-by-step workflow**:

1. **Process mixed file types**:
```
Request: "Convert all documents in /company-docs/ to Markdown"

Claude processes:
Scanning /company-docs/...
Found 87 files across 8 formats

Processing:
PDFs (32 files):
  ✓ employee-handbook.pdf
  ✓ safety-guidelines.pdf
  ...
  ✓ financial-report-q4.pdf

Word Documents (24 files):
  ✓ process-documentation.docx
  ✓ meeting-minutes.docx
  ...

PowerPoint (18 files):
  ✓ product-training.pptx
  ✓ sales-deck.pptx
  ...

Excel (8 files):
  ✓ budget-2024.xlsx
  ✓ inventory.xlsx
  ...

Images (5 files) - OCR applied:
  ✓ scanned-form.png
  ✓ whiteboard-photo.jpg
  ...

Total: 87 files processed
Success: 85 files (97.7%)
Failed: 2 files (corrupt/unsupported)
Output: /company-docs/markdown/
Total size: 24.3 MB → 8.7 MB (Markdown)
```

2. **Organize output**:
```
Request: "Organize converted files by document type"

Claude organizes:
✓ Created /company-docs/markdown/handbooks/
✓ Created /company-docs/markdown/reports/
✓ Created /company-docs/markdown/presentations/
✓ Created /company-docs/markdown/data/
✓ Created /company-docs/markdown/forms/

Files sorted by type:
- Handbooks: 8 files
- Reports: 32 files
- Presentations: 18 files
- Data/Spreadsheets: 8 files
- Forms (OCR): 19 files
```

3. **Create index**:
```
Request: "Create an index file listing all converted documents"

Claude generates:
```

**index.md**:
```markdown
# Company Documents Index

Generated: 2024-12-18
Total Documents: 85

## Handbooks

- [Employee Handbook](handbooks/employee-handbook.md) - 45 pages
- [Safety Guidelines](handbooks/safety-guidelines.md) - 23 pages
- [IT Security Policy](handbooks/it-security-policy.md) - 18 pages
...

## Reports

### Financial
- [Q4 2024 Financial Report](reports/financial-report-q4.md)
- [Annual Budget 2024](reports/annual-budget-2024.md)
...

### Operations
- [Monthly Operations Report Dec](reports/ops-report-dec.md)
...

## Presentations

### Training
- [Product Training](presentations/product-training.md) - 42 slides
- [Sales Methodology](presentations/sales-deck.md) - 28 slides
...

## Data

- [Budget 2024](data/budget-2024.md)
- [Inventory](data/inventory.md)
...

## Forms

- [Employee Onboarding Form](forms/onboarding-form.md)
- [Expense Report Template](forms/expense-report.md)
...
```

**Expected outcome**:
- Complete document library converted
- Organized by type
- Searchable and linkable
- Ready for knowledge base
- Dramatically reduced file size

---

## Advanced Features

### Azure Document Intelligence

**When to use**:
- Complex PDF layouts
- Scanned documents
- Forms and tables
- Multi-column text
- Handwritten text

**Configuration**:
```python
from markitdown import MarkItDown

md = MarkItDown(
    azure_doc_intelligence_endpoint="https://your-resource.cognitiveservices.azure.com",
    azure_doc_intelligence_key="your-key-here"
)

result = md.convert("complex-document.pdf")
```

**Benefits**:
- 95%+ accuracy on complex layouts
- Table structure preservation
- Form field extraction
- Handwriting recognition

---

### LLM-Powered Image Descriptions

**When to use**:
- Important images in documents
- Presentations with visual content
- Accessibility requirements
- Rich context needed

**Configuration**:
```python
from markitdown import MarkItDown

md = MarkItDown(
    llm_model="gpt-4o",  # or gpt-4o-mini
    llm_client=None       # Uses default OpenAI client
)

result = md.convert("presentation.pptx")
```

**Output**:
```markdown
![Chart showing quarterly revenue growth](image1.png)
*Description: A line chart displaying revenue growth over four quarters,
with Q4 showing the highest peak at $4.2M, representing a 14% increase from Q3.*

![Product photograph](image2.png)
*Description: Professional product photo of a silver laptop with a 15-inch display,
shown at a 45-degree angle against a white background.*
```

---

## Performance Optimization

### File Size Recommendations

| File Size | Processing | Recommendation |
|-----------|-----------|----------------|
| < 10 MB | Fast (< 5s) | Standard processing |
| 10-100 MB | Medium (5-30s) | Use streaming if available |
| 100 MB+ | Slow (> 30s) | Consider splitting or compression |

---

### Batch Processing Tips

```python
import os
from markitdown import MarkItDown
from concurrent.futures import ThreadPoolExecutor

md = MarkItDown()

def convert_file(filepath):
    result = md.convert(filepath)
    output = filepath.replace('.pdf', '.md')
    with open(output, 'w') as f:
        f.write(result.text_content)

# Process files in parallel
files = [f for f in os.listdir('.') if f.endswith('.pdf')]
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(convert_file, files)
```

---

### Memory Management

**For large files**:
```python
# Use streaming instead of loading entire file
with open("large-file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```

---

## Best Practices

### 1. Choose Right Tool for File Type

```
✅ GOOD:
- PDF → MarkItDown (excellent)
- Word → MarkItDown (excellent)
- Scanned image → MarkItDown + Azure OCR (best)
- Complex tables → Azure Document Intelligence

❌ SUBOPTIMAL:
- Large images → Basic OCR (use Azure instead)
- Corrupted PDF → Standard conversion (may fail)
```

---

### 2. Pre-Process Files

```
✅ GOOD:
- Compress large PDFs before conversion
- Rotate scanned images correctly
- Clean up temp files after processing

❌ BAD:
- Convert password-protected PDFs (will fail)
- Process corrupted files (waste time)
```

---

### 3. Organize Output

```
✅ GOOD:
input/
  reports/
    report1.pdf
output/
  reports/
    report1.md

❌ BAD:
everything-in-one-folder/
  file1.pdf
  file1.md
  file2.pdf
  file2.md
```

---

### 4. Validate Conversion Quality

```python
# Check conversion success
result = md.convert("document.pdf")

if len(result.text_content) < 100:
    print("⚠ Warning: Conversion may have failed (too little text)")

# Verify key content present
if "expected keyword" not in result.text_content:
    print("⚠ Warning: Expected content missing")
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions
- [reference.md](reference.md) - Complete API reference
- [GitHub Repository](https://github.com/microsoft/markitdown)
- [Azure Document Intelligence](https://azure.microsoft.com/products/ai-services/ai-document-intelligence)

---

## Quick Reference

### Common Commands

```bash
# Single file
"Convert document.pdf to Markdown"
"Extract text from spreadsheet.xlsx"
"Transcribe audio.mp3"

# Batch
"Convert all PDFs in /docs/"
"Process all Word documents"
"Transcribe all audio files"

# Advanced
"Use Azure OCR on scanned-form.png"
"Convert presentation with image descriptions"
"Extract tables from complex PDF"
```

---

## Troubleshooting

### Issue: "Conversion failed" or empty output
- Check file isn't corrupted
- Verify file format is supported
- Try opening file in native app first
- Check file permissions

### Issue: "Memory error" on large file
- Use `convert_stream()` instead of `convert()`
- Process file in chunks
- Increase available memory
- Compress file before conversion

### Issue: "Poor OCR quality"
- Increase image resolution
- Improve contrast/brightness
- Use Azure Document Intelligence
- Check image isn't rotated
- Verify text isn't too small

### Issue: "Missing tables or structure"
- Use Azure Document Intelligence for complex PDFs
- Verify source document is well-formatted
- Check PDF isn't just scanned image

---

## Questions?

**Q: What's the best format for LLM consumption?**
A: Markdown is ideal - structured, compact, and LLM-friendly. MarkItDown optimizes for this use case.

**Q: Can I convert password-protected PDFs?**
A: No, unlock PDFs before conversion.

**Q: Does it work offline?**
A: Basic conversion yes. Azure features and LLM descriptions require internet.

**Q: How accurate is OCR?**
A: 85-95% with basic OCR, 95-99% with Azure Document Intelligence.

**Q: Can I customize output format?**
A: Yes, process the Markdown output with additional Python code.

**Q: What about non-English documents?**
A: Supported! Works with many languages, especially with Azure AI.
