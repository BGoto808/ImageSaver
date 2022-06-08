# ImageSaver 📩
When sharing pictures, Discord doesn't allow users to download multiple images at a time-- which can be time consuming when dealing with many images. The ImageSaver Discord bot allows users to download multiple images automatically based on timestamp or number of messages. Currently in development and not released. Images are read from text-channel and downloaded into user's Downloads folder. 

## Content
- [Commands](https://github.com/BGoto808/ImageSaver/tree/main#commands)
- [Examples](https://github.com/BGoto808/ImageSaver/tree/main#examples)

## Commands
- .help : Display help menu
- .ping : Writes pong to text-channel as a test command
- .save : Saves image(s). Can be used with command-line argument parameters
    - Parameters:
        - t : Save based on time { Year: y, Month: m, Day: d, Hour: h, Minute: i, Second: s }
        - m : Save based on number of messages

## Examples

Commands that save images based on timestamp and number of messages
```
.save -t 8h    // Save images within last 8 hours
.save -t 15d   // Save images within last 15 days
.save -t 30i   // Save images within last 30 minutes
.save -m 100   // Save images within 100 messages
```
