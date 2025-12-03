# 🌈✨ Ctrl_Alt_Delighted: TimePal Local Setup Guide ✨🌈
Welcome to the best Flask website project EVER!
If you are here, you're probably ready to run our site locally and feel like a total tech princess. Let's get you all set up and ready to slay 💅💻

Step 1. Download the Project 

    Because this is a local-run project, start by grabbing the ZIP file. 
    
    1. Click the green "Code" button on GitHub 
    
    2. Hit "Download ZIP" 

    3. Unzip it like the absolute CHAMP you are 🫶
    
    4. Open the folder in Terminal (or in a coding software if you like ✨aesthetic coding✨)
    
      macOS/Linux :  cd /path/to/Ctrl_Alt_Delighted--main
      
      Windows  :  cd "C:\path\to\Ctrl_Alt_Delighted--main"

Step 2. Make Sure Python3 is Installed 
    1. Run: 
        macOS/Linux : python3 --version
        Windows : python --version
    If you see a version number like 3.x.x, you are all set 😚
    If not, download Python here: 
        👉 https://www.python.org/downloads/
    Make sure Windows users check the box "Add Python to PATH" during install. That is super, super      important 🙂‍↕️
    
Step 3: Install the required packages 
    These are the tools our website uses behind the scenes 
    Run: 
        macOS/Linux : pip3 install flask flask_sqlalchemy flask_wtf email_validator
        Windows : pip install flask flask_sqlalchemy flask_wtf email_validator

Step 4: (macOS + Linux only) Make sure your PATH includes Python's local bin 
    If your computer ever says: 
        flask: command not found
    Just add your local Python bin folder to PATH : 
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        source ~/.bashrc
    Or for zsh users: 
        echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
    Windows users usually don't need this step 🥳 🤩

Step 5: Run the Website!
    Inside the project folder, start the server: 
        flask --app main run
    Or if you are in your ✨developer era✨:
        flask --app main run --debug
    Your terminal should show something like: 
         * Running on http://127.0.0.1:5000
    Open that link in your broswer and BOOM! Website time! 🤯 😮 🙌

👏👏👏 You are all set! 👏👏👏
Your local setup is ready and running, great job!
Thanks for checking out our project, and feel free to reach out if you need help or want to contribute. Happy coding 😄💛✨

