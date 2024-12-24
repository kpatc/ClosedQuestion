
# ClosedQuestion

This project provides a FastAPI application capable of predicting whether a Stack Overflow question is closed or not, based on a custom machine learning model developed specifically for this task.

## Table of Contents

- [Overview](#overview)
- [Project Directory Structure](#project-directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

The goal of this project is to deliver a simple and efficient web service that analyzes Stack Overflow questions and predicts their status (open/closed). The backend is built using **FastAPI** and leverages a trained machine learning model for predictions.

## Project Directory Structure

The main structure of the project is as follows:

```
ClosedQuestion/
│
├── app.py               # FastAPI application for making predictions
├── data/
│   ├── cleaning.py      # Script for data cleaning
│   ├── scrap.py         # Script for data scraping
│
├── model/
│   ├── id2-ml-project(1).ipynb  # Notebook for model development
│   ├── model.json        # Model structure and parameters
│
├── Dockerfile           # Dockerfile for containerizing the project
├── LICENSE              # Project license
├── requirements.txt     # Python dependencies
├── .gitignore           # Files ignored by Git
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kpatc/ClosedQuestion/
   cd ClosedQuestion
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI application:**
   ```bash
   uvicorn app:app --reload
   ```

   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Usage

### Main Endpoint

- **`POST /predict`**: Submits a question and returns a prediction.  
  Example input JSON:
  ```json
  {
    "title": "How to reverse a list in Python?",
    "body": "I want to reverse a list in Python. Any suggestions?"
  }
  ```
  Example response JSON:
  ```json
  {
    "prediction": "open",
    "confidence": 0.87
  }
  ```

## Contributing

Contributions are welcome! If you have suggestions, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
