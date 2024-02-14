from queue import Queue, Empty


class TranscodingQueue:
    """
    Manages a queue of MediaFiles waiting to be transcoded.
    """
    def __init__(self):
        """
        Constructor for the class. Initializes the queue attribute.
        """
        self.queue = Queue()

    def add_to_queue(self, media_file):
        """
        Add the given media file to the queue.

        :param media_file: the media file to be added to the queue
        :return: None
        """
        self.queue.put(media_file)

    def get_next_media_file(self, timeout=None):
        try:
            return self.queue.get(block=True, timeout=timeout)
        except Empty:
            return None
