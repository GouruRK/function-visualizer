<h1 align="center">
  <br>
  function-visualiser
  <br>
</h1>

<h4 align="center">A python project to visualize mathematical function</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#next-step">Next step</a> •
  <a href="#license">License</a>
</p>

<p align="center">
 <img src="https://github.com/GouruRK/function-visualizer/blob/main/screenshots/Capture.PNG">
</p>

## Key Features

* Allows the user to plot any function, or the function derivative.
* Everthing is reziable. The user can set custom intervals, modify the size of the window, etc

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/) and [Tkinter](https://docs.python.org/3/library/tkinter.html). From your command line:

```bash
# Clone this repository
$ git clone https://github.com/GouruRK/function-visualizer.git

# Go into the repository
$ cd function-visualizer

# Run the app
$ python3 graphic.py 'your functions'
```

This project support basic operators, such as:
- '+'
- '-'
- '/'
- '*'
- '^' (for power)

### Precisions
- All functions arguments must be `'x'`.
- All functions must be written between quote marks (`''`).
- To plot a function derivatives, you just need to add `d` before the function expression.
- To draw multiple function, just add a space between two expressions.
- Parentheses are supported.

### Settings
All default settings are written in the `settings.py` file.
You can modify them to customize the graphic.

```py
X_MIN = -5     # The smallest abscissa
X_MAX = 5      # The biggest abscissa
Y_MIN = -5     # The smallest ordinate
Y_MAX = 5      # The biggest ordinate
STEP = 0.001   # The gap between each point
WIDTH = 400    # The width of the window
HEIGHT = 400   # The height of the window
AXES = True    # True to display the axes, False to hide them
```

The `FUNCTIONS = []` parameters will be automaticly modify depending on your arguments given by command line.

### Examples

```bash
# Plot the funtion y=2+x
$ python3 graphic.py '2+x'

# Plot the function y=2/x derivatives
$ python3 graphic.py 'd2/x'

# Plot the function y=2x and his derivatives at the same time
$ python3 graphic.py '2*x' 'd2*x'
```
## Next step

This is just the begining of the project, and more things will be add, such as pre-define functions (cos, sin, exp, sqrt, log, etc). A nice way to do that, is by implementing the [shutting yard](https://en.wikipedia.org/wiki/Shunting_yard_algorithm) algorithm. This implementation will also help to define if a expression is valid or not.

An other possible upgrade is to add graduation on the axes, and an option to travel on the graph.
## License

MIT

---
This README.md file has been generated with [Amit Merchant](https://github.com/amitmerchant1990) template from [GitHub README Templates](https://www.readme-templates.com/) website.

