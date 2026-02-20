import express from "express";

const PORT = 3003;
const app = express();

app.use(express.json());

const users = new Map();
let nextId = 1;

app.post("/users", (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    return res.status(400).json({ message: "Name and email are required" });
  }

  const user = {
    id: nextId++,
    name,
    email,
  };

  users.set(user.id, user);
  return res.status(201).json(user);
});

app.get("/users", (req, res) => {
  const limit = Number(req.query.limit ?? 100);
  const offset = Number(req.query.offset ?? 0);

  const usersArray = Array.from(users.values());
  return res.json(usersArray.slice(offset, offset + limit));
});

app.get("/users/:id", (req, res) => {
  const id = Number(req.params.id);
  const user = users.get(id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  return res.json(user);
});

app.put("/users/:id", (req, res) => {
  const id = Number(req.params.id);
  const user = users.get(id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  const { name, email } = req.body;

  if (name) user.name = name;
  if (email) user.email = email;

  return res.json(user);
});

app.delete("/users/:id", (req, res) => {
  const id = Number(req.params.id);
  const user = users.get(id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  users.delete(id);
  return res.status(204).send();
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
