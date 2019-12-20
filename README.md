# Run tensorboard in codes

## how to use

```python
from code_tensorboard import TensorBoardThread
import threading

tb_port = 6006
tb_host = 'localhost'
while True:
    signal = threading.Event()
    tb_thread = TensorBoardThread(signal, tb_path, tb_port)
    tb_thread.start()
    signal.wait()
    if tb_thread.wrong:
        tb_thread.terminate()
        tb_port += 1

print("http://{}:{}".format(tb_host, tb_port))
```

using this signal to wait, so you can use the url as soon as the start of tensorboard.