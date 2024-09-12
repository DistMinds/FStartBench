'use strict';

const express = require('express');
const Mustache = require('mustache');
const fs = require('fs');

const filename = "template.html";
const local_path = "./";

function random(b, e) {
    return Math.round(Math.random() * (e - b) + b);
}

// Handler function
async function handler(event, context = null) {
    let username = "entropy";
    let size = 1000;

    var random_numbers = new Array(size);
    for(var i = 0; i < size; ++i) {
        random_numbers[i] = random(0, 100);
    }

    var input = {
        cur_time: new Date().toLocaleString(),
        username: username,
        random_numbers: random_numbers
    };

    try {
        const template = await fs.promises.readFile(local_path + filename, "utf-8");
        const result = Mustache.render(template, input);
        return { "result": result };
    } catch (err) {
        return { "result": "Error processing template" };
    }
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

