#include <Python.h>

// Function 1: A simple 'hello world' function
static PyObject* helloworld(PyObject* self, PyObject* args)
{
    printf("Hello World\n");
    return Py_None;
}

// Function 2: A C fibonacci implementation
// this is nothing special and looks exactly
// like a normal C version of fibonacci would look
int Cfib(int n)
{
    if (n < 2)
        return n;
    else
        return Cfib(n-1)+Cfib(n-2);
}
// Our Python binding to our C function
// This will take one and only one non-keyword argument
static PyObject* fib(PyObject* self, PyObject* args)
{
    // instantiate our `n` value
    int n;
    // if our `n` value
    if(!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    // return our computed fib number
    return Py_BuildValue("i", Cfib(n));
}


// First one without help. This one takes unreasobably long in Python
// Small utility function to quickly and convinetly find the opponent number
int Copponent(int playerno)
{
    if(playerno==1) return 2;
    return 1;
}

static PyObject* opponent(PyObject* self, PyObject* args)
{
    int playerno;
    if(!PyArg_ParseTuple(args, "i", &playerno))
        return NULL;
    return Py_BuildValue("i", Copponent(playerno));
}


// Utility function to determine which weight is added to an edge when treating a board as a graph
int Cweight(int elem, int playerno) {
    if(elem==0) return 1;
    if(elem==playerno) return 0;
    return 1000;
}

static PyObject* weight(PyObject* self, PyObject* args)
{
    int elem, playerno;
    if(!PyArg_ParseTuple(args, "ii", &elem, &playerno))
        return NULL;
    return Py_BuildValue("i", Cweight(elem, playerno));
}




// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "helloworld", helloworld, METH_NOARGS, "Prints Hello World" },
    { "fib", fib, METH_VARARGS, "Computes the n'th fibonnachi number"},
    { "opponent", opponent, METH_VARARGS, "Quickly finds the opponent number"},
    { "weight", weight, METH_VARARGS, "Utility for treating board as graph"},
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Test Module",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_myModule(void)
{
    return PyModule_Create(&myModule);
}
