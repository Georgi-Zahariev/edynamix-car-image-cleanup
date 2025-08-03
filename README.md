# eDynamix Car Image Cleanup

**Cleanly extracts car images by removing backgrounds, preserving crisp edges, and eliminating reflections from mirrors and windows.**

## 🎯 Project Overview

This project provides a comprehensive solution for automotive image processing, specifically designed to create professional, catalog-ready car images with transparent backgrounds. The system handles complex challenges like reflective surfaces, glass areas, and edge artifacts that commonly occur in automotive photography.

## 🏗️ System Architecture

The project offers three different processing approaches:

### 1. **Basic Background Removal** (`main.py`)
- **Simple Mode**: Quick background removal using rembg
- **Advanced Mode**: Enhanced processing for reflective surfaces (windows, mirrors)
- **Use Case**: Fast batch processing for basic cleanup

### 2. **Complete Pipeline** (`app.py`) 
- **Background Removal**: AI-powered segmentation
- **Edge Refinement**: Advanced edge recovery and cleanup
- **Use Case**: Production-ready results with optimal quality

### 3. **LAMA Inpainting** (`run_lama_inpainting.py`)
- **Edge Detection**: Canny edge detection with customizable parameters
- **AI Inpainting**: State-of-the-art LAMA model for edge refinement
- **Use Case**: Professional-grade edge cleanup and artifact removal

## 🚀 Quick Start

### Prerequisites

```bash
# Create virtual environment
python3 -m venv car-cleanup-env
source car-cleanup-env/bin/activate  # On Windows: car-cleanup-env\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Usage

**Option 1: Basic Processing**
```bash
python main.py
# Processes all images in data/ folder
# Outputs: data/{filename}_removedbg.{ext}
```

**Option 2: Complete Pipeline**
```bash
python app.py
# Processes all images in data/ folder
# Outputs: outputs/{filename}_cleaned.png
```

**Option 3: LAMA Inpainting**
```bash
python run_lama_inpainting.py
# Processes all PNG files in outputs/ folder
# Outputs: outputs/{filename}_inpainted.png
```

## 📁 Project Structure

```
edynamix-car-image-cleanup/
├── main.py                    # Basic background removal
├── app.py                     # Complete processing pipeline
├── run_lama_inpainting.py     # LAMA-based edge refinement
├── src/
│   └── refine_edges.py        # Edge refinement utilities
├── data/                      # Input car images
├── outputs/                   # Final processed images
├── lama-cleaner/             # LAMA inpainting model
├── car-cleanup-env/          # Virtual environment
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Technical Features

### Background Removal
- **AI Segmentation**: Uses state-of-the-art models for accurate car detection
- **Transparent Output**: Preserves transparency for flexible use
- **Batch Processing**: Handles multiple images automatically

### Reflection Handling
- **Glass Detection**: Identifies semi-transparent areas (windows, mirrors)
- **Surface Conversion**: Converts reflections to dark, professional surfaces
- **Opacity Management**: Intelligent alpha channel processing

### Edge Refinement
- **Canny Edge Detection**: Precise boundary identification
- **Morphological Operations**: Cleanup and enhancement
- **AI Inpainting**: LAMA model for professional edge finishing

## 📊 Sample Results

| Input | Background Removed | Edge Refined | Final Output |
|-------|-------------------|--------------|--------------|
| `car1.jpg` | `car1_removedbg.jpg` | `car1_cleaned.png` | `car1_inpainted.png` |
| `car2.jpg` | `car2_removedbg.jpg` | `car2_cleaned.png` | `car2_inpainted.png` |
| `car3.jpg` | `car3_removedbg.jpg` | `car3_cleaned.png` | `car3_inpainted.png` |

## ⚙️ Configuration Options

### Main.py Modes
```python
MODE = "simple"    # Quick background removal
MODE = "advanced"  # Enhanced reflection handling
```

### LAMA Inpainting Parameters
```python
def generate_edge_mask(image_np, blur_radius=3, threshold=30):
    # blur_radius: Edge smoothing (1-10)
    # threshold: Edge sensitivity (10-100)
```

## 🎨 Use Cases

- **Automotive Websites**: Professional product images
- **Car Dealerships**: Consistent inventory photography
- **E-commerce Platforms**: Clean product presentations
- **Marketing Materials**: Catalog-ready visuals
- **Mobile Apps**: Optimized car images for listings

## 🔬 Technical Stack

- **Computer Vision**: OpenCV, PIL/Pillow
- **AI Models**: rembg, LAMA (Large Mask Inpainting)
- **Image Processing**: NumPy, advanced morphological operations
- **Background Removal**: State-of-the-art segmentation models
- **Edge Enhancement**: Canny detection + AI inpainting

## 📈 Performance

- **Processing Speed**: ~2-5 seconds per image (depending on size and method)
- **Quality**: Professional catalog-ready results
- **Batch Support**: Unlimited image processing
- **Memory Efficient**: Optimized for standard hardware

## 🛠️ Advanced Usage

### Custom Edge Parameters
```python
# In run_lama_inpainting.py
mask_np = generate_edge_mask(image_np, blur_radius=5, threshold=25)
```

### Reflection Handling
```python
# In main.py (advanced mode)
semi_transparent_mask = (alpha > 20) & (alpha < 220)
np_img[semi_transparent_mask, :3] = (30, 30, 30)  # Custom dark color
```

## 📋 Requirements

```
opencv-python>=4.5.0
numpy>=1.21.0
Pillow>=8.3.0
rembg>=2.0.0
iopaint>=1.0.0
torch>=1.9.0
```

## 🏢 Project Information

This project and research is part of the **eDynamix** project. Any further development was kept private.

---

## 📝 License

See [LICENSE](LICENSE) file for details.
