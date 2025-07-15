const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("🔥 Obaid Bhai ka Node.js App Render pe LIVE hai!");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
