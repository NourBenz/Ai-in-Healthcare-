# 📸 GUIDE TO ADDING IMAGES & CHARTS TO REPORTS

## Overview
This guide explains how to add images, charts, and visualizations to your markdown reports. It includes methods for local files, generated charts, and placeholders for manual additions.

---

## SECTION 1: ADDING IMAGES FROM FILES

### Method 1: Local Image Files

**Basic Syntax:**
```markdown
![Alt Text](path/to/image.png)
```

**Example:**
```markdown
![Feature Importance Chart](./charts/feature_importance.png)
```

### Method 2: Images with Custom Sizing

**Markdown with HTML (works in most viewers):**
```markdown
<img src="./charts/feature_importance.png" alt="Feature Importance" width="800" height="600">
```

### Method 3: Centered Images

```markdown
<div align="center">
  <img src="./charts/confusion_matrix.png" alt="Confusion Matrix" width="600" height="600">
  <p><i>Figure 1: Confusion Matrix for Random Forest Model</i></p>
</div>
```

### Recommended Image Locations:
```
AIProject/
├── reports/
│   ├── Q1_2026_Report.md
│   └── charts/
│       ├── feature_importance.png
│       ├── confusion_matrix.png
│       ├── roc_curve.png
│       ├── accuracy_comparison.png
│       ├── prediction_distribution.png
│       └── survival_by_stage.png
```

---

## SECTION 2: GENERATING CHARTS FROM YOUR DASHBOARD

### Generate Feature Importance Chart

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Assuming you have feature importance from Random Forest
features = ['Tumor Size', 'T Stage', 'N Stage', 'Grade', 'Regional Node Positive', 
            'Age', 'Estrogen Status', 'Progesterone Status', 'Regional Node Examined', 'A Stage']
importance = [0.2847, 0.2234, 0.1956, 0.1634, 0.1423, 0.0987, 0.0856, 0.0645, 0.0634, 0.0523]

plt.figure(figsize=(10, 6))
sns.barplot(x=importance, y=features, palette='husl')
plt.xlabel('Importance Score', fontsize=12)
plt.ylabel('Features', fontsize=12)
plt.title('Top 10 Most Important Features (Random Forest)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('./charts/feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Generate Confusion Matrix Heatmap

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Confusion matrix data
cm = np.array([[32, 3], [4, 0]])
labels = ['Alive', 'Dead']

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=labels, yticklabels=labels, cbar=False)
plt.xlabel('Predicted', fontsize=12)
plt.ylabel('Actual', fontsize=12)
plt.title('Confusion Matrix - Random Forest Model', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('./charts/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Generate Model Comparison Chart

```python
import matplotlib.pyplot as plt
import numpy as np

models = ['Logistic\nRegression', 'Random\nForest', 'K-Nearest\nNeighbors']
accuracy = [83.3, 85.2, 81.7]
f1_score = [75.2, 80.1, 72.6]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Accuracy comparison
ax1.bar(models, accuracy, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7, edgecolor='black')
ax1.set_ylabel('Accuracy (%)', fontsize=11)
ax1.set_title('Model Accuracy Comparison', fontsize=12, fontweight='bold')
ax1.set_ylim([70, 90])
ax1.axhline(y=80, color='red', linestyle='--', label='Target: 80%')
for i, v in enumerate(accuracy):
    ax1.text(i, v+1, f'{v}%', ha='center', fontweight='bold')

# F1-Score comparison
ax2.bar(models, f1_score, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7, edgecolor='black')
ax2.set_ylabel('F1-Score (%)', fontsize=11)
ax2.set_title('F1-Score Comparison', fontsize=12, fontweight='bold')
ax2.set_ylim([70, 85])
for i, v in enumerate(f1_score):
    ax2.text(i, v+1, f'{v}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('./charts/accuracy_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Generate ROC Curve

```python
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Assuming you have y_true and y_pred_proba
fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='#4ECDC4', lw=2.5, label=f'ROC Curve (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curve - Random Forest Model', fontsize=14, fontweight='bold')
plt.legend(loc='lower right', fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('./charts/roc_curve.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Generate Survival Distribution

```python
import matplotlib.pyplot as plt
import pandas as pd

# Sample survival data by stage
stages = ['Stage I', 'Stage II', 'Stage III', 'Stage IV']
survival_1yr = [98, 95, 88, 35]
survival_3yr = [96, 91, 79, 24]
survival_5yr = [95, 87, 72, 22]

x = np.arange(len(stages))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, survival_1yr, width, label='1-Year', color='#6BCB77')
ax.bar(x, survival_3yr, width, label='3-Year', color='#4D96FF')
ax.bar(x + width, survival_5yr, width, label='5-Year', color='#FF6B6B')

ax.set_ylabel('Survival Rate (%)', fontsize=12)
ax.set_xlabel('Stage', fontsize=12)
ax.set_title('Survival Rates by Stage', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(stages)
ax.legend()
ax.set_ylim([0, 105])

plt.tight_layout()
plt.savefig('./charts/survival_by_stage.png', dpi=300, bbox_inches='tight')
plt.close()
```

---

## SECTION 3: EMBEDDING CHARTS IN MARKDOWN

### Using Chart Placeholders

Add this to your report where you want the chart:

```markdown
### Feature Importance Analysis

The following chart shows the relative importance of each feature in the Random Forest model:

<div align="center">
  <img src="./charts/feature_importance.png" alt="Feature Importance Chart" width="800" height="600">
  <p><i>Figure 3: Top 10 Most Important Features - Random Forest Model</i></p>
  <p><b>Interpretation:</b> Tumor size and T stage account for 26% of model predictions combined.</p>
</div>
```

### With Description

```markdown
#### Model Performance Visualization

<div align="center">
  <img src="./charts/accuracy_comparison.png" alt="Model Comparison" width="900" height="400">
</div>

**Key Findings:**
- Random Forest achieved the highest accuracy at 85.2%
- All three models exceeded the 80% baseline target
- F1-scores show similar ranking to accuracy metrics
- Random Forest provides 2.1% improvement over Logistic Regression
```

---

## SECTION 4: CREATING TABLES WITH DATA

### Simple Markdown Table

```markdown
| Model | Accuracy | F1-Score | Precision | Recall |
|-------|----------|----------|-----------|--------|
| Logistic Regression | 83.3% | 75.2% | 81.5% | 73.8% |
| Random Forest | 85.2% | 80.1% | 84.3% | 79.5% |
| K-Nearest Neighbors | 81.7% | 72.6% | 79.8% | 71.4% |
```

### Table with Color Highlighting (HTML)

```html
<table>
  <tr style="background-color: #f0f0f0;">
    <th>Model</th>
    <th>Accuracy</th>
    <th style="color: #4ECDC4; font-weight: bold;">F1-Score</th>
  </tr>
  <tr>
    <td>Logistic Regression</td>
    <td>83.3%</td>
    <td style="background-color: #e8f4f8;">75.2%</td>
  </tr>
  <tr>
    <td><b>Random Forest</b></td>
    <td style="background-color: #c8e6c9;"><b>85.2%</b></td>
    <td style="background-color: #c8e6c9;"><b>80.1%</b></td>
  </tr>
  <tr>
    <td>K-Nearest Neighbors</td>
    <td>81.7%</td>
    <td style="background-color: #e8f4f8;">72.6%</td>
  </tr>
</table>
```

---

## SECTION 5: TEXT-BASED CHARTS & DIAGRAMS

### ASCII Art for System Architecture

```
┌─────────────────────────────────────────┐
│     Streamlit Web Dashboard (Port 8501) │
├─────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Dashboard│ │ Dataset  │ │ Predict  │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│  ┌──────────┐ ┌──────────┐             │
│  │ Patients │ │ Reports  │             │
│  └──────────┘ └──────────┘             │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│   ML Models Layer (scikit-learn)        │
├─────────────────────────────────────────┤
│  ┌──────────┐┌──────────┐┌──────────┐  │
│  │Logistic R││ RF Model ││   KNN    │  │
│  │egression ││          ││          │  │
│  └──────────┘└──────────┘└──────────┘  │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    Data Layer (pandas/numpy)            │
├─────────────────────────────────────────┤
│  Breast_Cancer.csv (196 records)        │
│  Features: Age, Stage, Size, etc.       │
└─────────────────────────────────────────┘
```

### Decision Tree Visualization

```
                    All Patients (196)
                          │
                          ├─ Tumor Size < 28mm? (median)
                          │   ├─ Yes → Stage I-II? 
                          │   │        └─ Mostly Alive
                          │   └─ No → Grade 3?
                          │           ├─ Yes → Higher Risk Dead
                          │           └─ No → Mixed Outcomes
```

---

## SECTION 6: FORMATTING BEST PRACTICES

### Color Codes for Reports

```markdown
🟢 GREEN (Success): #27AE60, #2ECC71, #6BCB77
- Achievements, passing tests, positive metrics

🔵 BLUE (Information): #3498DB, #4ECDC4, #5DADE2
- Data points, model information, features

🟠 ORANGE (Warning): #E67E22, #F39C12, #F59F00
- Issues requiring attention, cautions

🔴 RED (Critical): #E74C3C, #C0392B, #FF6B6B
- Failures, critical issues, errors

⚪ GRAY (Neutral): #95A5A6, #BDC3C7, #34495E
- Neutral information, secondary data
```

### Icon Usage

```markdown
✅ Completed / Success
⚠️ Warning / Attention needed
❌ Failed / Error
ℹ️ Information
🎯 Objective / Goal
📊 Data / Statistics
📈 Growth / Increase
📉 Decline / Decrease
🔍 Analysis / Investigation
💡 Insight / Idea
⭐ Important / Highlighted
🚀 Launch / Initiative
```

---

## SECTION 7: COMMON PLACEHOLDERS

### For Images You Need to Add Manually

```markdown
### Feature Correlation Heatmap

[PLACEHOLDER - INSERT CORRELATION MATRIX IMAGE HERE]

**Steps to Generate:**
1. Open your Jupyter notebook or Python script
2. Run: `sns.heatmap(df.corr(), annot=True)`
3. Save as PNG
4. Upload to ./charts/ folder
5. Replace placeholder with: `![Correlation Heatmap](./charts/correlation_heatmap.png)`
```

### For Charts from Dashboard

```markdown
### Prediction Distribution Chart

[PLACEHOLDER - SCREENSHOT FROM DASHBOARD > PATIENTS > DIAGNOSIS MIX]

**How to capture:**
1. Run: `streamlit run app.py`
2. Navigate to Patients page
3. Scroll to "Predicted Diagnosis Mix" section
4. Right-click chart → Save Image As
5. Save to ./charts/prediction_distribution.png
```

---

## SECTION 8: STEP-BY-STEP IMAGE INSERTION

### Create Directory Structure
```bash
mkdir -p ./reports/charts
cd ./reports
```

### Generate All Charts
```bash
python generate_charts.py
```

### Create Report File
```bash
# Create a new markdown file
touch Q1_2026_Report.md

# Or copy from template
cp REPORT_TEMPLATE.md Q1_2026_Report.md
```

### Edit Report
1. Open Q1_2026_Report.md in text editor
2. Replace all [PLACEHOLDERS] with actual data
3. Add chart references where needed:
   ```markdown
   ![Feature Importance](./charts/feature_importance.png)
   ```

### Convert to PDF (Optional)
```bash
# Install pandoc if not already installed
# https://pandoc.org/installing.html

# Convert markdown to PDF
pandoc Q1_2026_Report.md -o Q1_2026_Report.pdf --pdf-engine=xelatex

# Or use online tools:
# https://pandoc.org/try/
# https://markdown-to-pdf.com/
```

---

## SECTION 9: RECOMMENDED IMAGE SPECIFICATIONS

### Chart Dimensions
- **Line Charts:** 800×600 pixels
- **Bar Charts:** 800×600 pixels  
- **Pie Charts:** 600×600 pixels
- **Heatmaps:** 600×600 pixels
- **Composite (2+ charts):** 1000×600 pixels
- **Full-width Chart:** 1200×600 pixels

### File Format
- **Use PNG** for charts and screenshots (lossless)
- **Use JPG** only for photographs
- **Use SVG** for diagrams if possible (scalable)
- **DPI:** 300 DPI for professional printing, 72 DPI for web

### File Size
- Keep under 500KB per image for fast loading
- PNG with compression: typically 50-200KB
- Use tools to reduce size if needed: `pngquant`, `imagemin`

---

## SECTION 10: TOOLS & RESOURCES

### Charting Libraries

**Python Libraries:**
```python
import matplotlib.pyplot as plt      # Basic plotting
import seaborn as sns                # Statistical visualizations
import plotly.express as px          # Interactive charts
from sklearn.metrics import plot_confusion_matrix  # Model metrics
```

**Online Tools:**
- [Plotly Online Chart Editor](https://chart-studio.plotly.com/)
- [Google Charts](https://developers.google.com/chart)
- [Recharts (React)](https://recharts.org/)

### Image Tools

**Editing:**
- [Canva](https://www.canva.com/) - Design templates
- [GIMP](https://www.gimp.org/) - Free image editor
- [Figma](https://www.figma.com/) - Collaborative design

**Compression:**
- [TinyPNG](https://tinypng.com/) - PNG compression
- [ImageOptim](https://imageoptim.com/) - Mac
- [PNGCrush](https://pmt.sourceforge.io/pngcrush/) - Command line

### PDF Conversion

**Online:**
- [Pandoc Online](https://pandoc.org/try/)
- [CloudConvert](https://cloudconvert.com/)
- [Markdown to PDF](https://markdown-to-pdf.com/)

**Command Line:**
```bash
# Using Pandoc
pandoc report.md -o report.pdf

# Using wkhtmltopdf
wkhtmltopdf report.html report.pdf
```

---

## SECTION 11: EXAMPLE REPORT WITH IMAGES

### Complete Example

```markdown
# Q1 2026 Performance Report

## Executive Summary

[Summary text...]

## Model Performance

The following chart compares the performance of all three models:

<div align="center">
  <img src="./charts/accuracy_comparison.png" alt="Model Comparison" width="900" height="450">
  <p><i>Figure 1: Model Performance Comparison</i></p>
</div>

Key observations from the chart:
- Random Forest achieves highest accuracy at 85.2%
- All models exceed minimum 80% threshold
- [Additional interpretation...]

## Feature Importance

<div align="center">
  <img src="./charts/feature_importance.png" alt="Feature Importance" width="800" height="600">
  <p><i>Figure 2: Top 10 Feature Importance Scores</i></p>
</div>

The analysis reveals:
- Tumor size is the strongest predictor (28.5% importance)
- [Additional insights...]

## Prediction Outcomes

| Status | Count | Percentage |
|--------|-------|-----------|
| Alive | 74 | 85.1% |
| Dead | 13 | 14.9% |

[Additional tables and charts...]

## Appendix

See attached images in ./charts/ directory:
- accuracy_comparison.png
- feature_importance.png
- confusion_matrix.png
- roc_curve.png
```

---

## 💡 QUICK REFERENCE CHECKLIST

Before submitting your report:

- [ ] All [PLACEHOLDERS] replaced with actual data
- [ ] All images uploaded to ./charts/ directory
- [ ] Image paths correct in markdown: `./charts/image_name.png`
- [ ] All figures numbered and captioned
- [ ] Table data verified and formatted consistently
- [ ] Professional tone throughout
- [ ] Proofreading complete
- [ ] Charts saved at 300 DPI for printing
- [ ] File sizes under 500KB each
- [ ] PDF conversion tested (if needed)
- [ ] Approval obtained before distribution

---

**END OF GUIDE**

Use this guide to create professional, visually appealing reports!
