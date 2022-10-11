# π
## C extension

Build:
```bash
./setup.py build_ext --inplace
```

Run:
```
./example.py
```

## ctypes

Compile a shared library

```bash
gcc -shared approx_pi.c -o approx_pi.so
```

Run:
```
./example_ctypes.py
```

## swig

Auto generate c code:

```bash
swig -python pi_swig.i
```

Build the extension:

```bash
./setup-swig.py build_ext --inplace
```

Run:
```
./example_swig.py
```
