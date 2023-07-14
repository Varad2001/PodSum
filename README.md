# Podcast Summarizer

Podcast Summarizer is a Python project that allows you to extract and summarize the text content from podcasts. It supports podcasts from YouTube and Listen Notes platforms. The project utilizes web scraping, audio conversion, and natural language processing techniques to process the podcast audio files and generate a text summary.

## Features

- Extracts audio from YouTube videos and Listen Notes podcasts.
- Converts audio files to text using automatic speech recognition (ASR) using the Whisper ASR model.
- Supports downloading the podcast audio files and saving them to the specified directory.
- Summarizes the extracted text content using natural language processing techniques.

## Installation

Make sure to install Anaconda and git first.

1. Create a new Conda environment:

```
conda create -n podcast-summarizer python=3.9
conda activate podcast-summarizer
```

2. Clone the repository:

```
git clone https://github.com/your-username/podcast-summarizer.git
cd podcast-summarizer
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:

```
streamlit run app.py
```

2. Open your web browser and navigate to http://localhost:8501 to access the Podcast Summarizer interface.

3. Enter the podcast URL and click the "Extract Text" button to initiate the text extraction process. The extracted text will be displayed on the web interface.


## Disclaimer

This project is intended for educational purposes only and is provided as-is. The web scraping functionality included in this project may violate the terms of service of the platforms from which the podcast content is scraped. This project does not promote or encourage any commercial or unauthorized use of the podcast content. The responsibility for complying with the terms of service and applicable laws rests with the user of this project.
