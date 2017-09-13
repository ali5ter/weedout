
```
 /$$      /$$                           /$$        /$$$$$$              /$$    
| $$  /$ | $$                          | $$       /$$__  $$            | $$    
| $$ /$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$  \ $$ /$$   /$$ /$$$$$$  
| $$/$$ $$ $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$  | $$| $$  | $$|_  $$_/  
| $$$$_  $$$$| $$$$$$$$| $$$$$$$$| $$  | $$      | $$  | $$| $$  | $$  | $$    
| $$$/ \  $$$| $$_____/| $$_____/| $$  | $$      | $$  | $$| $$  | $$  | $$ /$$
| $$/   \  $$|  $$$$$$$|  $$$$$$$|  $$$$$$$      |  $$$$$$/|  $$$$$$/  |  $$$$/
|__/     \__/ \_______/ \_______/ \_______/       \______/  \______/    \___/  
```

# weedout RPi script
An RPi script to support Wen-Hao Tien's art installation, [Weed Out](https://www.wenhaotien.com/weed-out/).

The script simply plays an audio file based on the state of a GPIO pin input.

## Process
* Wen-Hao handles production of audio files on iPhone or in GarageBand and
exports as mpeg4 (m4a) files.
* She will ssh these resulting files to a directory, `~/audio`, on a
Rasberry Pi (RPi) 3 Model B.
* This script, aleady downloaded to the RPi, can be run or may already be
running.
* The script detects the first depression of a push switch via one of its
GPIO pins, randmoly selects an audio file from said directory and plays it
* The script detects when the push switch is released before allowing another
audio to be played. This will avoid playing lots of audio files while the
switch is depressed.
* Longer audio files are allowed to play simultaneously with newly started
audio files.

## Software requirements
To play m4a audio files:

    sudo apt-get install vlc-nox
    cvlc /pat/to/your/file.m4a

## Hardware configuration
An RPi is used to run this script. The circuit used to connect the switch to the RPi follows.

    3.3v -------.
                |
               [ ] 10K pull up resistor (red, black, orange)
                |
                |---------- GPIO input pin
                |
                 \ push switch
                |
    GND --------'

The 'pull up' resistor ensures the voltage on the GPIO pin is not floating: It will wither be 0v (GND) when pressed or 3.3v when open. The GPIO pin is initialized as an Input so the script can check if it is False (or GPIO.LOW)
to detect if push switch pressed.

## Running the script
Just run the `weedout.py` script, like this

    ./weedout.py

or to keep it running after logging out, use

    nohup python ./weedout.py &

To run it at start up edit the crontab, using

    sudo crontab -e

and add the line

    @reboot python /path/to/your/weedout.py &

By default, any m4a files found in the `./audio` directory will be played. If
an audio file hasn't finished playing before another is started, they will play
simultaeously.

While the script is meant to run on a RPi, it will also run on macOS but
simulate the GPIO input state using a random number. Test audio files are
included. This way the code function can be tested outside of an RPi.

## Configuration options
The configuration can be controlled using environment variables.

* `WO_AUDIO_DIR`: directory location of the audio files. Defaults to `./audio`
* `WO_AUDIO_TYPE`: type of audio file to play. Defaults to `m4a`
* `WO_CYCLE_TIME`: how often to check for input state of GPIO pin. Defaults to `0.1` seconds
* `WO_SINGLE_PLAY`: play a single audio file at a time. Defaults to `False`
* `WO_GPIO_PIN`: the GPIO pin number to check the input state of. Defaults to `23`

### How to change what directory to use for audio files
    export WO_AUDIO_DIR='/path/to/audio_dir'
    ./weedout.py

## TODO
* Investigate how to run script on RPi using [supervisor](http://supervisord.org/introduction.html)

## References
* [Wen-Hao Tien website](https://www.wenhaotien.com/weed-out/)
* [*Exibitions, Wen-hao Tien: WeedOut*](https://www.newartcenter.org/galleries/exhibit.aspx?id=1113), New Art Center in Newton
* [*Weeding Out The Obvious*](https://artscopemagazine.com/2017/08/weeding-out-the-obvious-wen-hao-tien-in-newton/), ArtScope
* Audio files for testing are provided royalty free from [SoundBible](http://soundbible.com/)

