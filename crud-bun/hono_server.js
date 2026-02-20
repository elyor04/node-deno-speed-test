import { Hono } from "hono";

const PORT = 3003;
const app = new Hono();

const users = new Map();
let nextId = 1;

app.post("/users", async (c) => {
  const { name, email } = await c.req.json();

  if (!name || !email) {
    return c.json({ message: "Name and email are required" }, 400);
  }

  const user = {
    id: nextId++,
    name,
    email,
  };

  users.set(user.id, user);
  return c.json(user, 201);
});

app.get("/users", (c) => {
  const limit = Number(c.req.query("limit") ?? 100);
  const offset = Number(c.req.query("offset") ?? 0);

  const usersArray = Array.from(users.values());
  return c.json(usersArray.slice(offset, offset + limit));
});

app.get("/users/:id", (c) => {
  const id = Number(c.req.param("id"));
  const user = users.get(id);

  if (!user) {
    return c.json({ message: "User not found" }, 404);
  }

  return c.json(user);
});

app.put("/users/:id", async (c) => {
  const id = Number(c.req.param("id"));
  const user = users.get(id);

  if (!user) {
    return c.json({ message: "User not found" }, 404);
  }

  const { name, email } = await c.req.json();

  if (name) user.name = name;
  if (email) user.email = email;

  return c.json(user);
});

app.delete("/users/:id", (c) => {
  const id = Number(c.req.param("id"));
  const user = users.get(id);

  if (!user) {
    return c.json({ message: "User not found" }, 404);
  }

  users.delete(id);
  return c.body(null, 204);
});

Bun.serve({ port: PORT, fetch: app.fetch });
console.log(`Server is running on http://localhost:${PORT}`);
