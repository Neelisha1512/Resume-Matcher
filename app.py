import gradio as gr
from api.app import app  # Import your Flask app

def run_flask():
    app.run(host='0.0.0.0', port=7860)

if __name__ == "__main__":
    run_flask()
