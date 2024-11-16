<!-- # PyMiner
This is a tool for mining and extracting metrics from Python open source projects on GitHub for empirical research.


comando para aumentar o buffer do git:

git config --global http.postBuffer 524288000 -->
# PyMiner - Python Feature Counter

Python Feature Counter is a tool designed to analyze Python repositories and count occurrences of specific Python language features introduced in various versions. The application processes repositories from a given list and generates detailed CSV reports with the analysis results.

---

## Features

- Analyzes Git repositories for occurrences of modern Python features.
- Supports multithreaded processing for better performance.
- Filters commits by date range.
- Outputs results in CSV format for easy reporting and visualization.

---

## Requirements

- **Python**: Version 3.12 or newer.
- **Git**: Must be installed and accessible in the system's PATH.
- **Dependencies**: Installable via `pip`.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/feature-counter.git
   cd feature-counter
   ´´´

2. Install dependencies:
    
   ```bash
   pip install -r requirements.txt
   ´´´

## Directory Structure

PyMiner/
├── visitors/                     # Feature-specific visitor modules
├── results/                      # Output directory for CSV files
├── main.py                       # Main script
├── feature_counter.py            # Core processing logic
├── requirements.txt              # Dependency file
└── README.md                     # Documentation

## Usage

1. Prepare the Input CSV File

The application expects a CSV file with a single column named name, containing the list of repositories to analyze in the format <owner>/<repo>. Example:

| name          |
|---------------|
| owner1/repo1  |
| owner2/repo2  |

Save the file as python-projects.csv or any name of your choice.

2. Run the Application

Run the script with the path to your CSV file as a command-line argument:

   ```bash
   python3 main.py python-projects.csv
   ´´´
3. Results

Processed results are saved in the results/ directory as CSV files, named <owner>_<repo>.csv. Each file includes:

    Repository details.
    Date range of commits analyzed.
    Count of specific Python feature occurrences.

## Configuration

The application can be customized directly in the script:

    start_date: Defines the earliest commit date to analyze. Default is 2012-01-01.
    max_threads: Sets the number of threads for parallel processing. Default is 4.
    steps: Specifies the number of days between commit analyses. Default is 30.