'use strict';

const express = require('express');
const tesseract = require('tesseractocr');

// Constants
const PORT = 9000;
const HOST = '0.0.0.0';

// File and Path Constants
const filename = "exodia.png";
const local_path = "./";

// OCR function
function ocr(key) {
    return new Promise((resolve, reject) => {
        tesseract.recognize(Buffer.from(key, "base64"), (err, text) => {
            if (err) {
                resolve({
                    statusCode: 500,
                    body: "Error!"
                });
            } else {
                resolve({
                    statusCode: 200,
                    body: text
                });
            }
        });
    });
}

// Handler function
async function handler(event, context = null) {
    try {
        const response = await ocr(local_path + filename);
        return { "result": response.body };  // 返回识别的文本
    } catch (error) {
        return { "result": "Error processing OCR" };
    }
}
// Main function
function main(params) {
    return handler(params, null);
}

exports.main = main;

// Web function invocation
const app = express();
app.get('/*', async (req, res) => {
    try {
        const response = await main({});
        res.send(response);
    } catch (err) {
        res.status(500).send('Error processing request');
    }
});

// Event function invocation
app.post('/event-invoke', async (req, res) => {
    try {
        const response = await main({});
        res.send(response);
    } catch (err) {
        res.status(500).send('Error processing request');
    }
});

var server = app.listen(PORT, HOST);
console.log(`SCF Running on http://${HOST}:${PORT}`);

server.timeout = 0; // never timeout
server.keepAliveTimeout = 0; // keepalive, never timeout
