# Hybo

###### Unofficial pure-python module for iLidar, solid state lidar by [Hybo](https://www.hybo.co/)

# Install
```bash
$ pip install hybo
```

# Example
### example 1: enter/exit block style
example/simple.py
```python
import time
import hybo

with hybo.Lidar('/dev/cu.usbserial-D3095E6S') as hybo:
    # waiting for connection
    time.sleep(1)
    
    # retrieve latest frame
    frame = hybo.get_latest_frame()
    print(frame)
```

### example 2: sequencial style
example/simple_sequencial.py
```python
import time
import hybo

SERIAL_DEV = '/dev/cu.usbserial-D3095E6S'

hybo = hybo.Lidar(SERIAL_DEV)
hybo.start()

# waiting for first frame
time.sleep(1)

print(hybo.get_latest_frame())
hybo.close()
```

### Result - it's the same for either.
```python
{'sequence': 53247, 'time_peak': 529.675937, 'points': array([[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0],
       ...,
       [0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]], dtype=int16)}
```

# TODO
- [ ] callback-style frame capturing
- [ ] frame queuing
- [ ] async mode
- [ ] better documentation