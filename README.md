![](https://i.ibb.co/fGKBbxy/NIC2-Banner-1.png)

# NIC2
NIC2 (Neural Interface for Control of Computers) is BCI project done by Gianluca Tarantino, from L.S. Amaldi in Italy, that partecipates to the Italian Olimpics of Robotics 2022.

- [Project Title](#project-title)
- [Description](#description)
- [Installation and usage](#installation-and-usage)
- [Development](#development)
- [Contribute](#contribute)
- [License](#license) 

## Description

NIC2, which stands for Neural Interface for Control of Computers, is a project that has the goal to control,
via serial communication, robotics and computers in general.

## Installation and usage

Before you start using NIC2, you have to download the repository and install all the Python depencencies, as they are listed in requirements.txt.
This is designed to run on a Raspberry Pi, but you can run it on any machine that supports Python with serial communication. \
After installing dependencies, to start the detection and the recognition you have to run `main.py`

``` bash
python3 src/main.py
```

## Development

The project has been developed with the following technologies:

- Arduino
- Raspberry Pi
- Python
- Numpy
- Scipy

and an ADS1299 and a SEN-13723, both connected to an Arduino Mega that has been used to detect the EEG and EMG data.

The data from the Arduino Mega are sent to the computer via USB serial communication, and read by the computer with the `serial` library in Python.\
Then on the EEG data are applied three filters: Low pass, High pass and Notch filter. Finally, cross-correlation is used to recognize where sample brain signals are in the detected values. To affine detection, cross-correlation is applied between the signal and various samples, to get which one is the most similar.

EMG data are passed as is, since they are already parsed by the SEN-13723 as a value between 0 and 1023, that represents the muscle activity.

These data can then be used to comand other robotics and computers in general.

## Contribute

To contribute you can freely open a push request or send me an email, to [gianlutara@gmail.com](mailto:gianlutara@gmail.com)

## License

[GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)
