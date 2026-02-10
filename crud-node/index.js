import { createServer } from "http";

// Fake database
const users = [];
let nextId = 1;

// Helper to parse JSON body
const parseBody = (req) => {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk.toString();
    });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(error);
      }
    });
    req.on("error", reject);
  });
};

// Helper to send JSON response
const sendJSON = (res, statusCode, data) => {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
};

// Router
const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const path = url.pathname;
  const method = req.method;

  try {
    // POST /users - CREATE
    if (method === "POST" && path === "/users") {
      const { name, email } = await parseBody(req);

      if (!name || !email) {
        return sendJSON(res, 400, { message: "Name and email are required" });
      }

      const user = {
        id: nextId++,
        name,
        email,
      };

      users.push(user);
      return sendJSON(res, 201, user);
    }

    // GET /users - READ ALL
    if (method === "GET" && path === "/users") {
      return sendJSON(res, 200, users);
    }

    // GET /users/:id - READ ONE
    if (method === "GET" && path.startsWith("/users/")) {
      const id = Number(path.split("/")[2]);
      const user = users.find((u) => u.id === id);

      if (!user) {
        return sendJSON(res, 404, { message: "User not found" });
      }

      return sendJSON(res, 200, user);
    }

    // PUT /users/:id - UPDATE
    if (method === "PUT" && path.startsWith("/users/")) {
      const id = Number(path.split("/")[2]);
      const user = users.find((u) => u.id === id);

      if (!user) {
        return sendJSON(res, 404, { message: "User not found" });
      }

      const { name, email } = await parseBody(req);

      if (name) user.name = name;
      if (email) user.email = email;

      return sendJSON(res, 200, user);
    }

    // DELETE /users/:id - DELETE
    if (method === "DELETE" && path.startsWith("/users/")) {
      const id = Number(path.split("/")[2]);
      const index = users.findIndex((u) => u.id === id);

      if (index === -1) {
        return sendJSON(res, 404, { message: "User not found" });
      }

      users.splice(index, 1);
      res.writeHead(204);
      return res.end();
    }

    // 404 - Route not found
    sendJSON(res, 404, { message: "Route not found" });
  } catch (error) {
    sendJSON(res, 500, { message: "Internal server error" });
  }
});

// Start server
const PORT = 3001;
server.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
