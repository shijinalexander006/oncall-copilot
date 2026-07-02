require("dotenv").config();
const express = require("express");
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: "development",
  integrations: [Sentry.expressIntegration()],
});

const app = express();
app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "demo-shop-api" });
});

app.post("/checkout", (req, res) => {
  const shouldFail = Math.random() < 0.3;
  if (shouldFail) {
    throw new Error("Payment failed: card declined");
  }
  res.json({
    status: "paid",
    amount: req.body.amount ?? 0,
  });
});

app.get("/break", (req, res) => {
  throw new Error("Forced outage for testing");
});

// New Sentry v8+ way — must be AFTER all routes
Sentry.setupExpressErrorHandler(app);

const port = process.env.PORT || 3001;
app.listen(port, () => {
  console.log(`Demo API running at http://localhost:${port}`);
});