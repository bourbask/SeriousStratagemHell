import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

app.get("/api/message", (req, res) => {
  res.json({ message: "Hello from the backend !" });
});

app.get("/api/message_2", (req, res) => {
  res.json({ message: "Plop." });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
