'use strict';

const express = require('express');
const Zip = new require('node-zip')();
const Jimp = require("jimp");

const filename = "exodia.png";
const local_path = "./";

class Image {
    constructor(url) {
        this.url = url;
    }

    generate() {
        return new Promise((resolve, reject) => {
            Jimp.read(this.url, (error, image) => {
                if (error) {
                    var response = {
                        statusCode: 200,
                        body: "AAAAA"
                    };
                    resolve(response);
                }
                var images = [];
                images.push(image.resize(196, 196).getBufferAsync(Jimp.AUTO).then(result => {
                    return {
                        size: "xxxhdpi",
                        data: result
                    };
                }));
                images.push(image.resize(144, 144).getBufferAsync(Jimp.AUTO).then(result => {
                    return {
                        size: "xxhdpi",
                        data: result
                    };
                }));
                images.push(image.resize(96, 96).getBufferAsync(Jimp.AUTO).then(result => {
                    return {
                        size: "xhdpi",
                        data: result
                    };
                }));
                images.push(image.resize(72, 72).getBufferAsync(Jimp.AUTO).then(result => {
                    return {
                        size: "hdpi",
                        data: result
                    };
                }));
                images.push(image.resize(48, 48).getBufferAsync(Jimp.AUTO).then(result => {
                    return {
                        size: "mdpi",
                        data: result
                    };
                }));
                Promise.all(images).then(data => {
                    for (var i = 0; i < data.length; i++) {
                        Zip.file(data[i].size + "/icon.png", data[i].data);
                    }
                    var d = Zip.generate({ base64: true, compression: "DEFLATE" });
                    var response = {
                        headers: {
                            "Content-Type": "application/zip",
                            "Content-Disposition": "attachment; filename=android.zip"
                        },
                        body: d
                    };
                    resolve(response);
                });
            });
        });
    }
}

async function handler(event, context = null) {
    var i = new Image(local_path + filename);
    return await i.generate();
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

