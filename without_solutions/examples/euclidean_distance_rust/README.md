# Quickstart

* Clone
* Build the rust extension (omit `--release` for an unoptimized debug
  build):
  ```bash
  cargo build --release
  ```
  Then move the resulting library in `target/release` to folder
   `.` containing the python script and name it `euclidean_distance.so`
  (`euclidean_distance.pyd` on windows).
  
  For unix only, there is a script doing build and move
  automatically:
  
  ```bash
  ./build-inplace.sh
  ```

* Call the extension from python:
  ```bash
  ./example.py
  ```
