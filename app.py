import asyncio
import os
import atexit
import time
from flask import Flask, render_template, request, send_file
from download_images import download_images
from zip_utils import zip_folder

app = Flask(__name__)

# Dictionary to store the download time of each folder
download_times = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        folder_name = request.form['name']
        asyncio.run(download_images(url, f'cache/{folder_name}'))
        zip_folder(folder_name)

        # Store the download time of the folder
        download_times[folder_name] = time.time()

        # Schedule deletion of the folder after 5 minutes

        return send_file(f'cache/{folder_name}.zip', as_attachment=True)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))