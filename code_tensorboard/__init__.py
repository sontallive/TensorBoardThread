import logging
import threading
from tensorboard import program, default
from tensorboard.program import TensorBoard


# override the launch function to get the service
class customTensorBoard(TensorBoard):

    def launch(self):
        """Python API for launching TensorBoard.

        This method is the same as main() except it launches TensorBoard in
        a separate permanent thread. The configure() method must be called
        first.

        Returns:
          The URL of the TensorBoard web server.

        :rtype: str
        """
        # Make it easy to run TensorBoard inside other programs, e.g. Colab.
        server = self._make_server()
        thread = threading.Thread(target=server.serve_forever, name='TensorBoard')
        thread.daemon = True
        thread.start()
        self.server = server
        return server.get_url()


# simulate the launch of tensorboard program
class TensorBoardTool:

    def __init__(self, dir_path, port=6006):
        self.dir_path = dir_path
        self.port = port

    def run(self):
        # Remove http message
        log = logging.getLogger('werkzeug').setLevel(logging.ERROR)
        # Start tensorboard server
        tb = customTensorBoard(default.get_plugins()+default.get_dynamic_plugins(),
                               program.get_default_assets_zip_provider())

        tb.configure(argv=[None, '--logdir', self.dir_path, '--port', str(self.port)])
        url = tb.launch()
        self.tb = tb
        return url


# the tensorboard should run in another thread
# and when the thread exits, the service shutdown
class TensorBoardThread(threading.Thread):
    def __init__(self, signal, dir_path, port=6006):
        threading.Thread.__init__(self)
        self.tb_tool = TensorBoardTool(dir_path, port)
        self.signal = signal
        self.url = None
        self.running = True
        self.wrong = False

    def run(self):
        try:
            self.url = self.tb_tool.run()
        except Exception:
            self.wrong = True
        self.signal.set()
        while self.running:
            pass
        self.tb_tool.tb.server.shutdown()

    def terminate(self):
        self.running = False
