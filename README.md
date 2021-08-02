# Wallpaper-changer

A program written in Python that changes the desktop wallpaper selecting a **random wallpaper** from [Reddit](https://www.reddit.com/r/wallpaper/), accessing the Reddit API with PRAW.

It's simple, first it takes a random wallpaper url using the *Python Reddit API Wrapper*, and then it downloads it. After that, it stores it in a folder that can be specified by command line arguments, and tells the system to use it as a wallpaper. This last part was the complicated, as different platforms have different mechanisms, and I managed to make it work for **Ubuntu and Windows**.

Appart from that, the program also stores some wallpapers in a "no-wifi" folder to have some in case the user is not connected. If that folder is empty, the program will use instead a previous wallpaper from the main folder.

You can change the default properties by passing them from the command line.

## How to use
1. Clone this repository or download the .zip file form github
2. Install the required python modules with the command `pip install -r requirements.txt` in windows or `pip3 install -r requirements.txt` in linux
3. ## Register a Reddit app
    Log into Reddit, head over to the Reddit app preferences page, and click ‘create an app’.
  Give it whatever name you’d like and select the script type.Finally, Reddit apps require a redirect URI. You won’t be using it however, so just put in a dummy one, such as http://www.example.com/
4. Add your Reddit app credentials to a .env file in the project directory, with two variables: CLIENT_ID and CLIENT_SECRET
5. Run `main.py` with python and it should work

### Change Wallpaper on startup
#### Ubuntu
- Go to the `wallpaper.sh` file in this project and edit it so it references to the correct python interpreter and the correct folder (you can also specify some arguments)
- Go to the app "Startup Applications" and click add
- When it prompts "Add Startup Program" put a name and a comment of your preference and then select a *command* by clicking on **browse**.
- After that, select the bash file `wallpaper.sh` and it's done!
#### Windows
1. Open the project folder
2. Create a shortcut to the `wallpaper.bat` file.
3. Once the shortcut is created, right-click the shortcut file and select Cut.
4. Press Start, type Run, and press Enter.
5. In the Run window, type shell:startup to open the Startup folder. Once the Startup folder is opened, click the Home tab at the top of the folder. Then, select Paste to paste the shortcut file into the Startup folder.

## Quotes wallpapers
- I've added a script that downloads powerful quotes wallpapers from [Quotefancy](https://quotefancy.com/) and sets it as a wallpaper. You just have to run it.