# Contagem Rua

## Usage Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/rafaeltb/contagem_rua.git
    ```
2. Navigate to the project directory:
    ```bash
    cd contagem_rua
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    streamlit run app.py
    ```

## Features
- Interactive visualization of street counting data.
- User-friendly interface to interact with real-time data.
- Integration with machine learning models to predict future counts.

## Deployment Guide
### Deploying on Streamlit Cloud
1. Push your changes to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Connect your GitHub repository.
4. Choose the `main` branch and deploy.

### Deploying on Hugging Face
1. Install the `transformers` library:
    ```bash
    pip install transformers
    ```
2. Create a new repo on [Hugging Face](https://huggingface.co/).
3. Push your code and models to the new repository.
4. Set up a `huggingface.yml` configuration file for deployment.