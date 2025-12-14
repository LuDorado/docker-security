let token = null;
const API_URL = "/api";

/* ---------- UI HELPERS ---------- */

function showView(id) {
  document.querySelectorAll(".view").forEach(v =>
    v.classList.remove("active")
  );

  const target = document.getElementById(id);
  if (target) target.classList.add("active");

  hideMessage();
}

function showMessage(text, type) {
  const m = document.getElementById("message");
  m.textContent = text;
  m.className = `message ${type}`;
}

function hideMessage() {
  const m = document.getElementById("message");
  m.className = "message hidden";
}

/* ---------- LOADER ---------- */

function showLoader(show = true) {
  const l = document.getElementById("loader");
  l.classList.toggle("show", show);
}

/* ---------- PASSWORD VALIDATION ---------- */

function validatePassword(password) {
  if (password.length < 10) return "Password must be at least 10 characters long";
  if (!/[a-z]/.test(password)) return "Password must contain at least one lowercase letter";
  if (!/[A-Z]/.test(password)) return "Password must contain at least one uppercase letter";
  if (!/[0-9]/.test(password)) return "Password must contain at least one number";
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) return "Password must contain at least one symbol";
  return null;
}

/* ---------- AUTH ---------- */

async function login(e) {
  e.preventDefault();
  showLoader(true);

  const form = e.target;
  const username = form.elements.username.value;
  const password = form.elements.password.value;

  try {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    localStorage.setItem("token", data.access_token);

    showMessage("Login successful", "success");
    setTimeout(() => showView("hacker"), 500);

  } catch {
    showMessage("Invalid username or password", "error");
  } finally {
    showLoader(false);
  }
}

async function register(e) {
  e.preventDefault();
  showLoader(true);

  const form = e.target;
  const username = form.elements.username.value;
  const password = form.elements.password.value;

  const passwordError = validatePassword(password);
  if (passwordError) {
    showMessage(passwordError, "error");
    showLoader(false);
    return;
  }

  try {
    const res = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) throw new Error();

    showMessage("User registered successfully", "success");
    setTimeout(() => showView("login"), 600);

  } catch {
    showMessage("Registration failed", "error");
  } finally {
    showLoader(false);
  }
}

function logout() {
  localStorage.removeItem("token");
  showView("login");
}

/* ---------- THEME ---------- */

function toggleTheme() {
  document.body.classList.toggle("dark");
}

/* ---------- INIT ---------- */

window.onload = () => {
  token = localStorage.getItem("token");

  if (token) {
    showView("hacker");
  } else {
    showView("welcome");
  }
};
