const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 4173;
const DIST_DIR = path.join(__dirname, 'ui', 'dist');
const PUBLIC_DIR = path.join(__dirname, 'ui', 'public');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.wasm': 'application/wasm',
  '.pdf': 'application/pdf',
  '.zip': 'application/zip',
  '.diff': 'text/plain; charset=utf-8',
  '.sql': 'text/plain; charset=utf-8',
  '.md': 'text/plain; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.c': 'text/plain; charset=utf-8',
  '.enc': 'application/octet-stream',
  '.so': 'application/octet-stream',
  '.exe': 'application/octet-stream'
};

const server = http.createServer((req, res) => {
  const urlPath = decodeURI(req.url.split('?')[0]);
  
  // Handle direct file paths or artifacts
  let filePath = path.join(DIST_DIR, urlPath === '/' ? 'index.html' : urlPath);

  // If requesting an artifact that might be in public/artifacts instead of dist
  if (urlPath.startsWith('/artifacts/')) {
    const artifactName = path.basename(urlPath);
    const distArtifact = path.join(DIST_DIR, 'artifacts', artifactName);
    const publicArtifact = path.join(PUBLIC_DIR, 'artifacts', artifactName);

    if (fs.existsSync(distArtifact) && fs.statSync(distArtifact).isFile()) {
      filePath = distArtifact;
    } else if (fs.existsSync(publicArtifact) && fs.statSync(publicArtifact).isFile()) {
      filePath = publicArtifact;
    }
  }

  fs.stat(filePath, (err, stats) => {
    const isArtifact = urlPath.startsWith('/artifacts/');

    if (err || !stats.isFile()) {
      if (isArtifact) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Artifact Not Found');
        return;
      }
      // SPA fallback
      filePath = path.join(DIST_DIR, 'index.html');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    const headers = {
      'Content-Type': contentType,
      'X-Content-Type-Options': 'nosniff'
    };

    if (isArtifact) {
      headers['Content-Disposition'] = `attachment; filename="${path.basename(filePath)}"`;
    }

    res.writeHead(200, headers);
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Chakravyuha CTF live on port ${PORT}`);
});
