
const port = 3000;

const express = require('express');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.post('/', (req, res) => {

    if (!req.body || !req.body.login || !req.body.login) {
        res.status(400);
        res.end();
        return;
    }

    if (req.body.login !== 'login' || req.body.password !== 'password') {
        res.status(401);
        res.end();
        return;
    }

    res.cookie('token', 'very secret token');
    res.status(200);
    res.end();
});

app.listen(port, () => {
    console.log(`Logging service is running on port ${port}`);
});