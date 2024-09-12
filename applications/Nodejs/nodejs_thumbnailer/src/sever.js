'use strict';

const express = require('express');
const sharp = require('sharp');
const fs = require('fs');
const https = require('follow-redirects').https;

const filename = "tesla.jpg";
const url = "https://github.com/spcl/serverless-benchmarks-data/blob/6a17a460f289e166abb47ea6298fb939e80e8beb/400.inference/411.image-recognition/fake-resnet/800px-20180630_Tesla_Model_S_70D_2015_midnight_blue_left_front.jpg?raw=true";
const local_path = "./";

function streamToPromise(stream) {
    return new Promise((resolve, reject) => {
        stream.on("close", () => resolve());
        stream.on("error", reject);
    });
}

async function handler(event, context = null) {
    let width = 1000;
    let height = 1000;

    const sharp_resizer = sharp().resize(width, height).png();
    var file = fs.createWriteStream(local_path + filename);

    https.get(url, (res) => {
        res.pipe(sharp_resizer).pipe(file);
    });

    let check = await streamToPromise(file).then(async () => {
        return new Promise((resolve, reject) => {
            fs.stat(local_path + filename, (err) => {
                if (err != null) {
                    resolve(false);
                } else {
                    resolve(true);
                }
            });
        });
    });

    return { "result": check };
}

// Constants
const PORT = 9000;
const HOST = '0.0.0.0';

// Web function invocation
const app = express();
app.get('/*', async (req, res) => {
    try {
        const response = await handler({});
        res.send(response);
    } catch (err) {
        res.status(500).send('Error processing request');
    }
});

// Event function invocation
app.post('/event-invoke', async (req, res) => {
    try {
        const response = await handler({});
        res.send(response);
    } catch (err) {
        res.status(500).send('Error processing request');
    }
});

var server = app.listen(PORT, HOST);
console.log(`SCF Running on http://${HOST}:${PORT}`);

server.timeout = 0; // never timeout
server.keepAliveTimeout = 0; // keepalive, never timeout

