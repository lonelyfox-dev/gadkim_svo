const express = require('express');
const axios = require('axios').default;
const app = express();
const port = 3000;

let modelTime = 0;

const services = new Proxy({}, {
    set(target, prop, val) {
        target[prop] = new Proxy(val, {
            set(target, prop, val) {
                target[prop] = val;
            }
        });

        return true;
    }
});

const events = new Proxy([], {
    set(target, prop, value) {
        target[prop] = value;

        target.sort((a, b) => a.eventTime - b.eventTime);

        return true;
    }
})

const sendTime = () => {
    if (services.reduce((res, el) => res && el.readyForEvent, true)) {
        modelTime = events[0] || 0;

        events.splice(0, 1);

        services.forEach(el => {
            el.readyForEvent = false;
            axios.get(`http://localhost:${el.port}/model-time?model-time=${modelTime}`);
        })
    }
}

app.get('/register', (req, res) => {
    services[req.query.serviceId] = {readyForEvent: false, port: req.query.port };
    console.log(services);
    res.status(200);
    res.end();
})

app.get('/ready-for-event', (req, res) => {
    services[req.query.serviceId].readyForEvent = true;
    res.status(200);
    res.end();
})

app.get('/new-event', (req, res) => {
    events.push(req.query.eventTime);
    res.status(200);
    res.end();
})

app.get('/model-time', (req, res) => {
    res.status(200).send(`${modelTime}`);
    res.end();
});

app.get('/next', (req, res) => {
    sendTime();
    res.end();
})

app.listen(port, () => {
    console.log(`Model time service is running on port ${port}`);
});