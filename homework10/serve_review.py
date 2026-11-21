"""Serve the local Homework 10 review with MP4 range support; loopback only."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import re

class ReviewHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range = None
        path = Path(self.translate_path(self.path))
        header = self.headers.get('Range')
        if header and path.is_file() and path.suffix.lower() == '.mp4':
            match = re.fullmatch(r'bytes=(\d+)-(\d*)', header)
            size = path.stat().st_size
            if match:
                start = int(match.group(1))
                end = min(int(match.group(2)) if match.group(2) else size - 1, size - 1)
                if start > end or start >= size:
                    self.send_error(416, 'Range not satisfiable')
                    return None
                f = path.open('rb')
                f.seek(start)
                self.byte_range = end - start + 1
                self.send_response(206)
                self.send_header('Content-Type', 'video/mp4')
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
                self.send_header('Content-Length', str(self.byte_range))
                self.end_headers()
                return f
        return super().send_head()

    def copyfile(self, source, outputfile):
        remaining = self.byte_range
        if remaining is None:
            return super().copyfile(source, outputfile)
        while remaining:
            data = source.read(min(65536, remaining))
            if not data:
                break
            outputfile.write(data)
            remaining -= len(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8770)
    args = parser.parse_args()
    root = str(Path(__file__).resolve().parent)
    ThreadingHTTPServer(('127.0.0.1', args.port), partial(ReviewHandler, directory=root)).serve_forever()
