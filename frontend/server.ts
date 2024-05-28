// server.ts

import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path';
import * as url from 'url';

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    let pathname = parsedUrl.pathname;
    if (pathname === '/') {
        pathname = '/index.html';
    }
    const filePath = path.join(__dirname, 'public', pathname);

    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('File not found');
            return;
        }
        res.writeHead(200);
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
