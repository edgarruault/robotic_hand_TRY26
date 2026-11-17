# Tendon-Driven Robotic Hand

A robotic hand prototype inspired by the human hand. The goal was to reproduce finger flexion and extension using cords as tendons and elastic bands to return the fingers to their open position.

## How It Works

- **Flexion.** A cord runs along the underside of each finger and winds onto an SG90 servo. As the servo winds the cord, the tension rotates the finger joints and curls the finger.
- **Extension.** Elastic bands connect the finger segments along the top of each finger. As the servo unwinds the cord, the tension drops and the bands pull the finger back open.

The CAD file `robo_hand.step` contains the model of one of the prototype's fingers.

## My Contribution

My main technical contribution was the embedded control system. The Arduino Nano receives keyboard commands over a USB serial connection at 9,600 baud and controls four servo outputs. Each channel can drive a servo in either direction or command it to stop. The Arduino acknowledges valid commands and returns all four outputs to neutral after more than 300 ms without a valid command.

I also took the lead on coordinating the project. I helped the team organize its work and encouraged each teammate to bring their strengths to the prototype.

## Keyboard Controls

The Python interface lets you select the Arduino's serial port and control each channel independently. Hold a key to move the corresponding servo and release it to return that channel to neutral. Press **S** to return all four channels to neutral.

| Arduino output | AZERTY keys |
| --- | --- |
| D3 | R / F |
| D5 | G / T |
| D7 | Y / H |
| D9 | U / J |

## Source Code

- [Arduino firmware](controle_servos/clavier_servos/clavier_servos/clavier_servos.ino) handles serial commands and drives the servos using the `Servo` library.
- [Python control interface](controle_servos/controle_clavier.py) provides a Tkinter interface and communicates over USB using `pyserial`.
