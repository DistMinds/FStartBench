'use strict';

const express = require('express');
const fs = require('fs');

const filename = "data.json";
const local_path = "./home/ubuntu/applications/RainbowCake-ASPLOS24/applications/nodejs_auto_complete/src/data.json";

// Binary Search function
const binarySearch = function (array, v) {
    let lo = -1, hi = array.length;
    const vlen = v.length;
    let mi = -1;
    var miv = null;
    var finished = false;

    while (1 + lo !== hi) {
        mi = lo + ((hi - lo) >> 1);
        miv = array[mi].substr(0, vlen);
        if (miv == v) {
            break;
        } else if (miv > v) {
            hi = mi;
        } else {
            lo = mi;
        }
    }

    if (mi > 0) {
        do {
            if (array[mi-1] < miv) {
                finished = true;
            } else {
                mi--
            }
        } while (mi > 0 && !finished);
    }
    return mi;
};

// Filter function
const filterStr = function(str) {
    return str.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").trim();
};

// Response function
const response = function(retval) {
    return {
        headers: { 'Content-Type':'application/json' }, 
        statusCode:200,
        body: Buffer.from(JSON.stringify(retval)).toString('base64')
    };
};

// Handler function
async function handler(event, context = null) {
    try {
        let term = "ikun";
        const arr = JSON.parse(fs.readFileSync(local_path + filename, 'utf8'));
        const MAX_RESULTS = 20;

        term = filterStr(term);
        const ind = binarySearch(arr, term);

        let retval = [];
        if (ind > -1) {
            for (let i = ind; i < arr.length; i++) { 
                if (arr[i].indexOf(term) !== 0) {
                    break;
                }
                
                let j = arr[i].indexOf('*');
                retval.push(arr[i].substr(j+1));

                if (retval.length === MAX_RESULTS) {
                    break;
                }
            }
        }

        return response(retval);
    } catch (err) {
        return response({ "error": "Error processing request" });
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

