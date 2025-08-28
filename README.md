# pyodide-cheat-sheet
A collection of useful code snippets for application development with [Pyodide](https://pyodide.org).

## Table of Contents
* [Loading Pyodide and running Python code](#loading-pyodide-and-running-python-code)
* [Returning the result of a Python expression](#returning-the-result-of-a-python-expression)
* [Loading a Python module and binding a function](#loading-a-python-module-and-binding-a-function)
* [Loading dependencies](#loading-dependencies)
* [Interaction with the DOM (Document Object Model)](#interaction-with-the-dom-document-object-model)
* [Interaction with the BOM (Browser Object Model)](#interaction-with-the-bom-browser-object-model)
* [Type translations between JavaScript and Python](#type-translations-between-javascript-and-python)
  * [JavaScript to Python (aka what Python functions receive via parameters)](#javascript-to-python-aka-what-python-functions-receive-via-parameters)
  * [Python to JavaScript (aka what Python functions return)](#python-to-javascript-aka-what-python-functions-return)
* [File system](#file-system)
  * [Upload files to the file system](#upload-files-to-the-file-system)
  * [Download files from the file system](#download-files-from-the-file-system)
* [Plotting](#plotting)
  * [matplotlib](#matplotlib)
  * [plotly](#plotly)

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

#### Example for passing mutable Python types (analogous to [previous example](#example-for-passing-mutable-javascript-types))
Python:
```python
def do_something(change_array_fn, call_function_fn):
    array = ["a", "b", "c", "d"]
    print(f"Array before: {array=}")
    change_array_fn("1234", 42, array)
    print(f"Array after: {array=}")

    obj = {
        "data": "Hello World!",
        "log": lambda s: print(s),
    }
    call_function_fn(obj)
```

JavaScript:
```javascript
async function run() {
    function changeArray(s, i, array) {
        console.log("s=", s, "i=", i, "array=", array.toJs());

        array[2] = i;
        array.push(s);
    }

    function callFunction(obj) {
        obj.log(obj.data);
    }

    (await pyodidePromise).runPython("do_something")(changeArray, callFunction);
}
run();
```

#### Example for explicit conversion (dict to Map)
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

## File system
`pyodide.FS` is an alias to [Emscripten's File System API](https://emscripten.org/docs/api_reference/Filesystem-API.html#id2). You can for instance find out that */home/pyodide* is current working directory via `pyodide.FS.cwd()`.

### Upload files to the file system
HTML:
```html
<input type="file" id="fileupload" />
<button onclick="uploadFile()">Upload file</button>
```

JavaScript:
```javascript
async function uploadFile() {
    const file = document.getElementById("fileupload").files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.fileName = file.name;
    reader.onload = async (event) => {
        const reader = event.target;
        const data = new Uint8Array(reader.result);

        const pyodide = await pyodidePromise;
        pyodide.FS.writeFile(reader.fileName, data);
        pyodide.runPython("print_file")(reader.fileName);
    }
    reader.readAsArrayBuffer(file);
}
```

Python:
```python
def print_file(file_name):
    with open(file_name, "r") as f:
        print(f"Reading from {file_name}")
        while line := f.readline():
            print(line)
```

### Download files from the file system
Python:
```python
def create_file():
    file_name = "text.txt"
    with open(file_name, "w") as f:
        for i in range(100):
            print(f"{i},{i*i}", file=f)

    return file_name
```

JavaScript:
```javascript
async function downloadFile() {
    pyodide = await pyodidePromise;
    fileName = pyodide.runPython("create_file")();

    // from https://stackoverflow.com/a/54468787
    const content = pyodide.FS.readFile(fileName);
    const a = document.createElement('a');
    a.download = fileName;
    a.href = URL.createObjectURL(new Blob([content], { type: "application/octet-stream" }));
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(a.href);
    document.body.removeChild(a);
}
downloadFile();
```

## Plotting
### matplotlib
The package [matplotlib-pyodide](https://github.com/pyodide/matplotlib-pyodide) is automatically loaded when loading *matplotlib* via micropip.

HTML:
```html
<div id="plotTarget"></div>
```

JavaScript:
```javascript
async function plot() {
    (await pyodidePromise).runPython("plot")("plotTarget");
}
plot();
```

Python:
```python
from js import document
import matplotlib.pyplot as plt


def plot(target):
    document.pyodideMplTarget = document.getElementById(target)

    #  from https://matplotlib.org/stable/users/explain/quick_start.html#a-simple-example
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

    plt.show()
```

### plotly
Load *plotly* and *pandas* via micropip.

HTML:
```html
<head>
    ...
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js" charset="utf-8"></script>
    ...
</head>
...
<div id="plotTarget"></div>
```

JavaScript:
```javascript
async function plot() {
    (await pyodidePromise).runPython("plot")("plotTarget");
}
plot();
```

Python:
```python
from js import document
import plotly.express as px


def plot(target):
    plot_output = document.getElementById(target)

    fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
    fig_html = fig.to_html(
        include_plotlyjs=False,
        full_html=False,
        default_height='350px'
    )
    render_plot(plot_output, fig_html)


#  from https://codepen.io/jmsmdy/pen/MWpdjVZ
def render_plot(container, plot_html):
    range = document.createRange()
    range.selectNode(container)
    document_fragment = range.createContextualFragment(plot_html)
    while container.hasChildNodes():
        container.removeChild(container.firstChild)
    container.appendChild(document_fragment)
    container.style = "width: 100%; height: 350px; overflow-y: scroll;"
```
