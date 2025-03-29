document.addEventListener("DOMContentLoaded", () => {
  // Signup functionality
  document.getElementById("signupForm")?.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Successfully Registered!");
    window.location.href = "login.html";
  });

  // Login functionality
  document.getElementById("loginForm")?.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Login Successful!");
    window.location.href = "index.html";
  });
});
