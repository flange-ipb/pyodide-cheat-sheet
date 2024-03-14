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
    await loadPyModule("module.py", pyodide)
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