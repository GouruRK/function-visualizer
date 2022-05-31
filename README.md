
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

![screenshot](screenshots/Capture.png)

## Key Features

Allows the user to plot any function, or the function derivative.


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
  

### Examples

```bash
# Plot the funtion y=2x
$ python3 graphic.py '2*x'

# Plot the function y=2x derivatives
$ python3 graphic.py 'd2*x'

# Plot the function y=2x and his derivatives at the same time
$ python3 graphic.py '2*x' 'd2*x'
```
## Next step
This is just the begining of the project, and more things will be add, such as pre-defined functions (cos, sin, exp, sqrt, log, etc). A nice way to do that, is by implementing the [shutting yard](https://en.wikipedia.org/wiki/Shunting_yard_algorithm) algorithm. This implementation will also help to defined if a expression is valid or not.
## License

MIT

---
This README.md file has been generated with [Amit Merchant](https://github.com/amitmerchant1990) template.

