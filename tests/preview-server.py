"""Preview static HTML from the .astro file without needing an Astro install.
Not a substitute for framework build verification.
"""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote
import mimetypes
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  p=unquote(self.path.split('?')[0]); target=(ROOT/'src/pages/index.astro') if p in ('/','/index.html') else (ROOT/'public'/p.lstrip('/')).resolve()
  if not target.is_file() or (p not in ('/','/index.html') and not target.is_relative_to(ROOT/'public')):
   self.send_error(404);return
  b=target.read_bytes();t='text/html' if target.suffix=='.astro' else (mimetypes.guess_type(str(target))[0] or 'application/octet-stream')
  self.send_response(200);self.send_header('Content-Type',t);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',4173),Handler).serve_forever()
