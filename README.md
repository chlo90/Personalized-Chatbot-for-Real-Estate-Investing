# Real Estate GPT for investing
This tool is designed to analyze real estate investments by calculating key financial metrics and assessing property details. 

The user will be able to see the pins of property locations on the map and they can ask a series of questions to the "Real Estate Consultant" for the best property to analyze and potentially buy.  
## Getting Started

### Prerequisites

 - langchain
 - streamlit
 - folium
 - pandas
 - python-dotenv

### Disclaimer for Web Scraping 
This tool includes functionality for web scraping from Redfin. 
 It is important to note that this feature is intended strictly for educational purposes only. Users are responsible for adhering to the terms of service of the websites they scrape, and this tool should not be used in a way that violates those terms or any applicable laws. Always obtain permission from website owners before scraping their sites.

### Setup
Follow these steps to set up your Python environment for running the scripts included in this repository. These instructions assume that Python 3 is already installed on your system.

1. Create a Virtual Environment
* On Mac:```python3 -m realestategpt```
* On Window: ```py -m venv realestategpt```

2. Sign up for OpenAI and get OPENAI API Key (platform.openai.com)

3. Create a .env file and put OpenAI API key values 
* ```OPENAI_API_KEY=**********************```
4. Install Python requirements in the project repository: 
* ```pip install -r requirements.txt```

This command will install all the Python packages listed in the requirements.txt file. These packages are necessary for the scripts to run properly.


## Activate the Virtual Environment:
* On macOS and Linux:
```.venv/bin/activate```
* On Windows:
```.venv\Scripts\activate```

Activating the virtual environment will change your shell’s prompt to show the name of the environment and modify the environment so that running python will get you that particular version and installation of Python.

## Deactivating the Virtual Environment
After you finish working in the virtual environment, you can deactivate it by running: deactivate

This command will revert your Python environment back to normal.

## Usage
Instructions on how to use the project or its features.



