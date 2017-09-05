
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
RPi script to support Wen-Hao Tien's art installation, Weed Out.

The script simply plays an audio file based on the state of a GPIO pin input.

## Process
Wen-Hao ssh's m4a files from her iPhone to RPi. To play m4a audio files:

    sudo apt-get install vlc-nox
    cvlc /pat/to/your/file.m4a

## Hardware configuration
The installation will feature a mementory switch connected to the RPi using the following circuit.

    3.3v -------.
                |
               [ ] 10K pull up resistor
                |
                |---------- GPIO input pin
                |
                 \ push switch
                |
    GND --------'

Pull up resistor used to make sure GPIO input pin is either 0v when pressed or GND when 3.3v when open. When GPIO pin is set up as an Input, we check if False (or GPIO.LOW) to detect if push switch pressed.

## Running the script
Just run the `weedout.py` script.

By default, any m4a files found in the `./audio` directory will be played. If an audio file hasn't finished playing before another is started, they will play simultaeously.

While the script is meant to run on a RPi, it will also run on macOS but simulate the GPIO input state using a random number. This way the code function can be tested outside of an RPi.

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

## References
* [New Art Center in Newton, Exhibitions,  Wen-hao Tien: Weed Out](https://www.newartcenter.org/galleries/exhibit.aspx?id=1113)
* [Wen-Hao Tien web site](https://www.wenhaotien.com/weed-out/)
* [ArtScope article](https://artscopemagazine.com/2017/08/weeding-out-the-obvious-wen-hao-tien-in-newton/)
* Audio file for testing from [SoundBible](http://soundbible.com/)

