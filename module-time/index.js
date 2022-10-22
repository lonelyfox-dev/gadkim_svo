const express = require('express');
const app = express();
require('express-ws')(app)
const port = 3000;

let events = [];

events = new Proxy(events, {
    set(target, prop, value) {
        target[prop] = value;

        target.sort((a, b) => a.eventTime - b.eventTime);

        return true;
    }
})

let services = [];

const sendTime = () => {
    if (services.reduce((res, el) => res && el.readyToGetTime, true)) {
        const modelTime = events[0]?.eventTime || 0;

        events.splice(0, 1);

        services.forEach(el => {
            el.readyToGetTime = false;
            el.socket.send(modelTime);
        })
    }
}

services = new Proxy(services, {
    set(target, prop, val) {
        target[prop] = new Proxy(val, {
            set(target, prop, val) {
                target[prop] = val;

                sendTime();
            }
        });

        sendTime();

        return true;
    }
});

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.get('/model-time', (req, res) => {
    res.send(modelTime);
});

app.ws('/model-time', (ws) => {
    ws.on('message', (messageStr) => {
        const message = JSON.parse(messageStr);

        switch (message.type) {
            case ('CONNECT'): {
                const {serviceId} = message.data;

                services[services.length - 1] = {socket: ws, serviceId, readyToGetTime: false};
                break;
            }
            case ('NEW_EVENT'): {
                const {eventTime} = message.data;

                events.push({eventTime});
                break;
            }
            case ('READY_FOR_EVENT'): {
                const {serviceId} = message.data;

                services.find(el => el.serviceId === serviceId).readyToGetTime = true;
                break;
            }
            default: {
                break;
            }
        }
    });

    services.push({});
    ws.send(0);
});

app.listen(port, () => {
    console.log(`Model time service is running on port ${port}`);
});