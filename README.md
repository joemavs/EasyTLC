# EasyTLC

EasyTLC is a Python-based image-processing application for analysing thin-layer chromatography (TLC) plates. It allows users to upload an image of a TLC plate, identify the plate boundaries, solvent front and baseline, and automatically calculate the retention factor ($R_f$) of detected spots.

The project was developed as part of a biomedical engineering design project investigating a low-cost method for screening cough syrup samples for potential ethylene glycol (EG) and diethylene glycol (DEG) contamination.

## Features

* Upload TLC plate images in common image formats
* Manually define the four corners of the TLC plate
* Automatically crop and process the selected plate
* Mark the solvent front and baseline
* Detect spots on the TLC plate using image processing
* Calculate the $R_f$ value of each detected spot
* Highlight spots falling within a specified $R_f$ range
* Display a warning when a potentially relevant spot is detected
* Simple graphical user interface built with Tkinter

## How It Works

The analysis follows the general workflow below:

1. **Upload an image** of a TLC plate.
2. **Select the four corners** of the plate to remove the surrounding background.
3. **Mark the solvent front** and **baseline**.
4. The application processes the cropped image and identifies visible spots.
5. The centroid of each detected spot is used to calculate its $R_f$ value.
6. Spots within the specified $R_f$ range are highlighted.
7. A warning is displayed if a potentially relevant spot is detected.

The default detection threshold is:

**$R_f$ = 0.35–0.55**

This range was selected during project testing as a favourable range for identifying EG, providing a true positive rate of approximately **0.91** and a false positive rate of approximately **0.21** in the evaluated dataset.

## Performance

Receiver operating characteristic (ROC) analysis gave the EasyTLC algorithm an **AUC of 0.928**, demonstrating strong discrimination between the tested TLC plates with and without EG.

However, the algorithm is not intended to provide definitive confirmation of contamination. False positives occurred when other TLC spots fell within the target $R_f$ range, and direct testing with DEG was not performed.

Potential future improvements include:

* Comparing sample TLC plates against a known uncontaminated control
* Improving image alignment to reduce errors caused by rotated plates
* Using watershed-based segmentation to separate merged spots
* Reducing variability in the measured $R_f$ values of EG and DEG

## Installation

### Requirements

* Python 3.0 or later
* Pillow
* OpenCV
* NumPy
* scikit-image
* Tkinter

Install the required Python packages with:

```bash
pip install Pillow opencv-python numpy scikit-image
```

> Tkinter is included with many standard Python installations. On some systems it may need to be installed separately.

## Running EasyTLC

Clone the repository or download the project files.

Navigate to the project directory:

```bash
cd EasyTLC
```

Run the application:

```bash
python main.py
```

The EasyTLC welcome screen should then appear.

## Using the Application

### 1. Upload a TLC image

Select **Upload TLC Image** and choose an image of the TLC plate.

Supported formats include common formats such as:

* PNG
* JPEG/JPG
* BMP
* GIF
* TIFF

### 2. Crop the TLC plate

Select the four corners of the TLC plate in order.

The selected points are displayed on the image and are used to define the region for analysis.

### 3. Select the solvent front

Mark the position of the solvent front on the plate.

### 4. Select the baseline

Mark the baseline from which the spots travelled.

### 5. Analyse the plate

EasyTLC processes the image and calculates the $R_f$ value of each detected spot.

Spots falling within the configured threshold range are highlighted and a warning is displayed.

## Project Structure

```text
EasyTLC/
├── main.py
├── ...
└── README.md
```

The application is organised into Python modules responsible for the graphical interface and image-processing workflow.

## Limitations

EasyTLC was developed as a prototype for low-cost TLC analysis and has several limitations:

* The user must manually identify the plate boundaries, baseline and solvent front.
* Image rotation can affect $R_f$ calculations.
* Overlapping or merged spots may be detected as a single spot.
* Other substances producing spots within the target $R_f$ range can result in false positives.
* Direct validation using DEG was not performed.
* Positive detections should therefore be treated as an indication for further investigation rather than definitive confirmation of contamination.

## Background

Ethylene glycol and diethylene glycol contamination of pharmaceutical products can pose serious safety risks. TLC provides a relatively low-cost analytical technique, but conventional analysis can require laboratory equipment and trained users.

EasyTLC explores whether image processing and a simple graphical interface can make TLC analysis more accessible while providing automated measurement of spot $R_f$ values.

## Technologies

* **Python**
* **Tkinter** – graphical user interface
* **OpenCV** – image processing
* **Pillow** – image handling
* **NumPy** – numerical processing
* **scikit-image** – image analysis

## Author

Developed as part of a Biomedical Engineering design project at **Imperial College London**.

## Disclaimer

EasyTLC is a research and educational prototype. It should not be used as a standalone diagnostic or regulatory testing method. Results should be confirmed using appropriate validated analytical techniques where required.
