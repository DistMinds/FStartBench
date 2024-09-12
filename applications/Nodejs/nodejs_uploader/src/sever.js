'use strict';

const express = require('express');
const fs = require('fs');
const https = require('follow-redirects').https;
const nano = require('nano')('http://whisk_admin:some_passw0rd@172.17.0.1:5984');

const filename = "hpx.zip";
const url = "https://github.com/STEllAR-GROUP/hpx/archive/1.4.0.zip";
const local_path = "./";

function streamToPromise(stream) {
    return new Promise((resolve, reject) => {
        stream.on("close", () => resolve());
        stream.on("error", reject);
    });
}

async function handler(event, context = null) {
    let db_name = "ul";
    let database;

    try {
        database = nano.use(db_name);
    } catch (e) {
        await nano.db.create(db_name);
        database = nano.use(db_name);
        await database.insert({ "success": true }, 'file');
    }

    var doc = await database.get('file');

    var file = fs.createWriteStream(local_path + filename);
    https.get(url, (res) => {
        res.pipe(file);
    });

    await streamToPromise(file).then(async () => {
        var data = fs.readFileSync(local_path + filename);
        try {
            await database.attachment.insert(doc._id, filename, data, "application/zip", { 'rev': doc._rev });
        } catch (e) {
            console.log(e);
        }
    });

    return { "result": doc };
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

