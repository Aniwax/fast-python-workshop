# Pi

Dependency: [pybind11](https://pybind11.readthedocs.io/en/stable/)

Compile extension:

```bash
c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` pi.cpp -o pi`python3-config --extension-suffix`
```

Then run:

```bash
./example.py
```
