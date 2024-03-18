# pyodide-cheat-sheet
A collection of useful code snippets for application development with [Pyodide](https://pyodide.org).

## Loading Pyodide and running Python code
HTML:
```html
<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>
    </head>
    <body>
        <script>
            const pyodidePromise = loadPyodide();

            async function helloWorld() {
                // logs "Hello World" on the JavaScript console
                (await pyodidePromise).runPython("print('Hello World')");
            }
            helloWorld();
        </script>
    </body>
</html>
```

## Returning the result of a Python expression
JavaScript:
```javascript
answer = (await pyodidePromise).runPython("int('101010', 2)");
console.log("Answer is:", answer);
```

## Loading a Python module and binding a function
Python (*module.py*):
```python
def greeting(name="unknown person"):
    print(f"Hello {name}!")
```

JavaScript:
```javascript
const pyodidePromise = startPyodide();

async function startPyodide() {
    const pyodide = await loadPyodide();
    await loadPyModule("module.py", pyodide);
    return pyodide;
}

async function loadPyModule(name, pyodide) {
    const response = await fetch(name);
    const code = await response.text();
    return pyodide.runPythonAsync(code);
}

async function greet() {
    const greetingFunction = (await pyodidePromise).runPython("greeting");
    greetingFunction("John Doe");
    greetingFunction();
}
greet();
```

Alternative: You can also [fetch and unpack an entire archive to the in-browser file system](https://pyodide.org/en/stable/usage/faq.html#how-can-i-load-external-files-in-pyodide) and [apply `pyodide.pyimport()`](https://pyodide.org/en/stable/usage/loading-custom-python-code.html#loading-then-importing-python-code).

## Loading dependencies
Pyodide offers a lightweight package installer called *micropip* that supports loading of [packages built in Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) and pure Python wheels from PyPI (file name ends with `-py3-none-any.whl`).

JavaScript:
```javascript
const pyodidePromise = startPyodide();

async function startPyodide() {
    const pyodide = await loadPyodide();

    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install(["numpy", "rdflib"]);

    await loadPyModule("module.py", pyodide);
    return pyodide;
}

async function loadPyModule(name, pyodide) {
    const response = await fetch(name);
    const code = await response.text();
    return pyodide.runPythonAsync(code);
}

async function doSomething() {
    (await pyodidePromise).runPython("calc_det")();
    graphInTurtleFormat = (await pyodidePromise).runPython("serialize_graph")();
    console.log(graphInTurtleFormat);
}
doSomething();
```

Python (*module.py*):
```python
import numpy as np
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF


def calc_det():
    a = np.array([[1, 2], [3, 4]])
    print(f"Determinant is {np.linalg.det(a)}")


def serialize_graph():
    g = Graph()

    alice = URIRef("http://example.org/alice")
    bob = URIRef("http://example.org/bob")

    g.add((alice, FOAF.name, Literal("Alice")))
    g.add((bob, FOAF.name, Literal("Bob")))
    g.add((alice, FOAF.knows, bob))

    return g.serialize()
```

## Interaction with the DOM (Document Object Model)
This is very similar to [how it's done in JavaScript](https://www.w3schools.com/js/js_htmldom.asp) with the `document` object.

Python:
```python
from js import document


def hello_world():
    h1 = document.createElement("h1")
    h1.innerText = "Hello World!"
    h1.style.color = "green"
    document.body.appendChild(h1)
```

## Interaction with the BOM (Browser Object Model)
This is very similar to [how it's done in JavaScript](https://www.w3schools.com/js/js_window.asp) with the `window` object.

Python:
```python
from js import window


def do_something():
    location = window.location.href
    width = window.screen.width
    height = window.screen.height

    window.alert(f"Welcome to {location}! Your window size is {width}x{height}.")
```

## Type translations between JavaScript and Python
### JavaScript to Python (aka what Python functions receive via parameters)
* immutable types: see [implicit conversions](https://pyodide.org/en/stable/usage/type-conversions.html#javascript-to-python)
* mutable types: see [explicit conversion of proxies](https://pyodide.org/en/stable/usage/type-conversions.html#type-translations-jsproxy-to-py)

#### Example
```javascript
async function doSomething() {
    array = ["a", "b", "c", "d"];
    console.log("Array before: ", array);
    (await pyodidePromise).runPython("change_array")("1234", 42, array);
    console.log("Array after: ", array);

    obj = {
        data: "Hello World",
        log: (s) => console.log(s),
    };
    (await pyodidePromise).runPython("call_function")(obj);
}
doSomething();
```

Python:
```python
def change_array(s: str, i: int, array: list):
    print(f"{s=} {i=} {array=}")

    array[2] = i
    array.append(s)


def call_function(obj):
    obj.log(obj.data)
```

### Python to JavaScript (aka what Python functions return)
* immutable types: see [implicit conversions](https://pyodide.org/en/stable/usage/type-conversions.html#python-to-javascript)
* mutable types: see [explicit conversion of proxies](https://pyodide.org/en/stable/usage/type-conversions.html#type-translations-pyproxy-to-js)

#### Example for explicit conversion (array)
```javascript
async function doSomething() {
    proxy = (await pyodidePromise).runPython("create_py_dict")();
    console.log("Map from create_py_dict(): ", proxy.toJs());

    map = (await pyodidePromise).runPython("create_js_map")();
    console.log("Map from create_js_map(): ", map);
}
doSomething();
```

Python:
```python
from pyodide.ffi import to_js


def create_py_dict():
    return {i : i*i for i in range(10)}


def create_js_map():
    return to_js({i : i * i * i for i in range(10)})
```
