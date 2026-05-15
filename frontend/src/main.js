import {
    login,
    register,
    getSkills,
    createSkill,
    deleteSkill,
    addLog,
    patchSkill
} from "./api.js";
import "./style.css";
import { confirmAction, showToast } from "./ui.js";

function checkAuth() {
    const token = localStorage.getItem("token");
    const path = window.location.pathname;

    const isLoginPage = path.includes("login");
    const isRegisterPage = path.includes("register");
    const isHomePage = path.includes("home");

    if (!token && isHomePage) {
        window.location.href = "/login.html";
        return;
    }

    if (token && (isLoginPage || isRegisterPage)) {
        window.location.href = "/home.html";
        return;
    }

    if (token && isHomePage) {
        viewSkills();
    }
}

document.addEventListener("DOMContentLoaded", checkAuth);

window.login = async function () {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const data = await login(username, password);
    
    if (!data?.access_token) return;

    localStorage.setItem("token", data.access_token);

    window.location.href = "/home.html";
};

window.logout = async function () {
    const ok = await confirmAction("Logout?");

    if (!ok) return;

    localStorage.removeItem("token");

    window.location.replace("/login.html");
};

window.register = async function () {
    const email = document.getElementById("register-email").value;
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    const data = await register({ email, username, password });

    

    window.location.href = "/login.html";
};

window.createSkill = async function () {
    const name = document.getElementById("skill-name").value;

    await createSkill(name, localStorage.getItem("token"));
    await viewSkills();
    showToast("Skill created successfully");
};

window.patchSkill = async function (id) {
    const name = document.getElementById(`skill-name-${id}`).value;
    
    await patchSkill(id, name, localStorage.getItem("token"));
    await viewSkills();
    showToast("Name updated successfully");
};

window.deleteSkill = async function (id) {
    console.log("DELETE CLICKED", id);
    const ok = await confirmAction("Delete skill?");
    console.log("CONFIRM OPENED");
    
    if (!ok) return;

    await deleteSkill(id, localStorage.getItem("token"));
    await viewSkills();
};

window.addLog = async function (id) {
    try {
        await addLog(id, localStorage.getItem("token"));
        await viewSkills();
        showToast("Log added successfully");
    } catch (err) {
        showToast("Failed to add log");
    }   
};

window.viewSkills = async function () {
    const data = await getSkills(localStorage.getItem("token"));

    const list = document.getElementById("skills-list");
    list.innerHTML = "";

    for (const skill of data) {
        const progress = skill.xp / skill.target * 100;
        
        const li = document.createElement("li");

        li.innerHTML = `
            <input id="skill-name-${skill.id}" value="${skill.name}" />
            <button onclick="addLog(${skill.id})">+</button>
            <button onclick="patchSkill(${skill.id})">Save</button>
            <button onclick="deleteSkill(${skill.id})">Delete</button>

            <div>
                Current: ${skill.current_streak} <br>
                Max: ${skill.max_streak}
            </div>

            <div style="width: 800px; background: #ddd;">
                <div style="width: ${progress}%; background: #c59700; height: 10px;"></div>
            </div>
            <div>
                Xp: ${skill.xp} / ${skill.target}
            </div>
        `;

        list.appendChild(li);
    }
};