const API_URL = "http://127.0.0.1:8000/api";

// -------------------- REGISTER --------------------
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
      role: document.getElementById("role").value,
    };
    try {
      const res = await fetch(`${API_URL}/auth/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (res.ok) {
        document.getElementById("message").innerText =
          "✅ Registered successfully! Redirecting to login...";
        setTimeout(() => {
          window.location.href = "/login/";
        }, 2000);
      } else {
        const result = await res.json();
        document.getElementById("message").innerText =
          "❌ Registration failed: " + (result.detail || "Check inputs");
      }
    } catch (err) {
      console.error(err);
      document.getElementById("message").innerText = "❌ Registration error!";
    }
  });
}

// -------------------- LOGIN --------------------
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      username: document.getElementById("loginUsername").value,
      password: document.getElementById("loginPassword").value,
    };
    try {
      const res = await fetch(`${API_URL}/auth/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await res.json();
      if (res.ok) {
        localStorage.setItem("access", result.access);
        document.getElementById("loginMessage").innerText =
          "✅ Login successful! Redirecting...";
        setTimeout(() => {
          window.location.href = "/profile/";
        }, 1500);
      } else {
        document.getElementById("loginMessage").innerText =
          "❌ Login failed: " + (result.detail || "Check credentials");
      }
    } catch (err) {
      console.error(err);
      document.getElementById("loginMessage").innerText = "❌ Login error!";
    }
  });
}

// -------------------- FETCH PROFILE --------------------
let currentProfileData = null; // keep profile data for editing

async function fetchProfile() {
  try {
    const token = localStorage.getItem("access");
    const res = await fetch(`${API_URL}/me/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    currentProfileData = data; // save globally

    let html = `
      <h2>My Profile</h2>
      <p><b>Username:</b> ${data.username}</p>
      <p><b>Email:</b> ${data.email}</p>
      <p><b>Role:</b> ${data.role}</p>
      <hr>
    `;

    if (data.role === "freelancer") {
      html += `
        <h3>Freelancer Details</h3>
        <p><b>Headline:</b> ${data.profile?.headline || "—"}</p>
        <p><b>Summary:</b> ${data.profile?.summary || "—"}</p>
        <p><b>Experience:</b> ${data.profile?.years_experience || 0} years</p>
        <p><b>Hourly Rate:</b> ${data.profile?.hourly_rate_expectation || "—"}</p>
        <p><b>Education:</b> ${data.profile?.education || "—"}</p>
        <p><b>Work Experience:</b> ${data.profile?.experience || "—"}</p>
        <p><b>Tech Stack:</b> ${data.profile?.tech_stack || "—"}</p>
        <p><b>Skills:</b> ${data.profile?.skills || "—"}</p>
      `;
    } else {
      html += `
        <h3>Recruiter Details</h3>
        <p><b>Company Name:</b> ${data.recruiter_profile?.company_name || "—"}</p>
        <p><b>Website:</b> ${data.recruiter_profile?.website || "—"}</p>
        <p><b>About:</b> ${data.recruiter_profile?.about || "—"}</p>
      `;
    }

    html += `<br><button onclick="showEditForm('${data.role}')">✏️ Edit Profile</button>`;
    document.getElementById("profileData").innerHTML = html;

  } catch (err) {
    console.error(err);
  }
}

// -------------------- UPDATE PROFILE --------------------
async function updateProfile(role) {
  const token = localStorage.getItem("access");

  const formData = {};
  if (role === "freelancer") {
    formData.headline = document.getElementById("headline").value;
    formData.summary = document.getElementById("summary").value;
    formData.years_experience = document.getElementById("years_experience").value;
    formData.hourly_rate_expectation = document.getElementById("hourly_rate_expectation").value;
    formData.education = document.getElementById("education").value;
    formData.experience = document.getElementById("experience").value;
    formData.tech_stack = document.getElementById("tech_stack").value;
    formData.skills = document.getElementById("skills").value;
  } else {
    formData.company_name = document.getElementById("company_name").value;
    formData.website = document.getElementById("website").value;
    formData.about = document.getElementById("about").value;
  }

  const endpoint =
    role === "freelancer"
      ? `${API_URL}/freelancer/profile/`
      : `${API_URL}/recruiter/profile/`;

  try {
    const res = await fetch(endpoint, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });

    if (res.ok) {
      alert("✅ Profile updated!");
      fetchProfile();
    } else {
      alert("❌ Failed to update profile!");
    }
  } catch (err) {
    console.error(err);
  }
}

// -------------------- SHOW EDIT FORM --------------------
function showEditForm(role) {
  let formHtml = "<h3>Edit Profile</h3>";

  if (role === "freelancer") {
    const p = currentProfileData?.profile || {};
    formHtml += `
      <label>Headline</label><input id="headline" value="${p.headline || ""}"><br>
      <label>Summary</label><textarea id="summary">${p.summary || ""}</textarea><br>
      <label>Experience (years)</label><input id="years_experience" type="number" value="${p.years_experience || 0}"><br>
      <label>Hourly Rate</label><input id="hourly_rate_expectation" type="number" value="${p.hourly_rate_expectation || ""}"><br>
      <label>Education</label><textarea id="education">${p.education || ""}</textarea><br>
      <label>Work Experience</label><textarea id="experience">${p.experience || ""}</textarea><br>
      <label>Tech Stack</label><textarea id="tech_stack">${p.tech_stack || ""}</textarea><br>
      <label>Skills</label><textarea id="skills">${p.skills || ""}</textarea><br>
    `;
  } else {
    const r = currentProfileData?.recruiter_profile || {};
    formHtml += `
      <label>Company Name</label><input id="company_name" value="${r.company_name || ""}"><br>
      <label>Website</label><input id="website" value="${r.website || ""}"><br>
      <label>About</label><textarea id="about">${r.about || ""}</textarea><br>
    `;
  }

  formHtml += `<button onclick="updateProfile('${role}')">Save</button>`;
  document.getElementById("profileData").innerHTML = formHtml;
}
