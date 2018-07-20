const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());
app.get('/', (req, res) => {
    res.send("This is my node server! Whoop!")
});

app.listen(process.env.NODE_PORT, () => {
  console.log("node.js -> Listening on port 3000")
});