// Fake database
const users = new Map();
let nextId = 1;

// Helper to send JSON response
const sendJSON = (status, data) => {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
};

// Request handler
const handler = async (req) => {
  const url = new URL(req.url);
  const path = url.pathname;
  const method = req.method;

  try {
    // POST /users - CREATE
    if (method === "POST" && path === "/users") {
      const { name, email } = await req.json();

      if (!name || !email) {
        return sendJSON(400, { message: "Name and email are required" });
      }

      const user = {
        id: nextId++,
        name,
        email,
      };

      users.set(user.id, user);
      return sendJSON(201, user);
    }

    // GET /users - READ ALL
    if (method === "GET" && path === "/users") {
      const limit = Number(url.searchParams.get("limit") ?? 100);
      const offset = Number(url.searchParams.get("offset") ?? 0);

      const usersArray = Array.from(users.values());
      return sendJSON(200, usersArray.slice(offset, offset + limit));
    }

    // GET /users/:id - READ ONE
    if (method === "GET" && path.startsWith("/users/")) {
      const id = Number(path.split("/")[2]);
      const user = users.get(id);

      if (!user) {
        return sendJSON(404, { message: "User not found" });
      }

      return sendJSON(200, user);
    }

    // PUT /users/:id - UPDATE
    if (method === "PUT" && path.startsWith("/users/")) {
      const id = Number(path.split("/")[2]);
      const user = users.get(id);

      if (!user) {
        return sendJSON(404, { message: "User not found" });
      }

      const { name, email } = await req.json();

      if (name) user.name = name;
      if (email) user.email = email;

      return sendJSON(200, user);
    }

    // DELETE /users/:id - DELETE
    if (method === "DELETE" && path.startsWith("/users/")) {
      const id = Number(path.split("/")[2]);
      const user = users.get(id);

      if (!user) {
        return sendJSON(404, { message: "User not found" });
      }

      users.delete(id);
      return new Response(null, { status: 204 });
    }

    // 404 - Route not found
    return sendJSON(404, { message: "Route not found" });
  } catch (error) {
    return sendJSON(500, { message: "Internal server error" });
  }
};

// Start server
const PORT = 3002;
Deno.serve({ port: PORT }, handler);
