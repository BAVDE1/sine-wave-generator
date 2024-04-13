# sine wave generator

Generates sine waves and displays them on a screen.

**Run `main.py` (made with python 3.11)**

---

8 different coloured pages of 4 modals each. 

Each modal generates a separate sine wave in its respective colour. Modals have change-able variables including:
- `amplitude` (size)
- `frequency` (speed)
- `phase` (offset) 

Modals can be `cleared` or `paused` (although pausing is a little scuffed).

Each modal also has its own 'circle' representation of its sine wave, which is purely visual.

The 'universal' modal can be used to change every value of every active modal to its own (all the variables above).
It can also remove every modal at once.

The separate `phase division` range can be used to vary the size of a phase for every modal (phase / div).

The display screen on which the modals' waves will render have a multitude of settings:
- `pixels / frame` (amount of pixels the display will scroll per frame)
- `line size` (thickness of lines between points)
- `point size` (size of each point)
- `granularity` (amount of points generated per the displays scroll amount)

The display screen can render either only the currently selected page or all pages (i.e. all active modals).

Note: this is python, so it will drop frames when more waves are being rendered at the same time.

---

### dev stuff


- (DONE) phase division inpt
- (DONE) clear btn on modal
- (DONE) n pages of modals
- (DONE) render selected page or all pages
- (DONE) universal modal
