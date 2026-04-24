import {
    login,
    register,
    getSkills,
    createSkill,
    deleteSkill,
    addLog,
    getStats,
    patchSkill
} from "./api.js";
import "./style.css";

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

window.logout = function () {
    if (!confirm("Are you sure you want to logout?")) return;

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
};

window.patchSkill = async function (id) {
    const name = document.getElementById(`skill-name-${id}`).value;
    
    await patchSkill(id, name, localStorage.getItem("token"));
    await viewSkills();
};

window.deleteSkill = async function (id) {
    if (!confirm("Are you sure you want to delete?")) return;

    await deleteSkill(id, localStorage.getItem("token"));
    await viewSkills();
};

window.addLog = async function (id) {
    try {
        await addLog(id, localStorage.getItem("token"));
        await viewSkills();
        alert("Log added!");
    } catch (err) {
        alert(err.message);
    }   
};

window.getStats = async function (id) {
    const data = await getStats(id, localStorage.getItem("token"));

    document.getElementById(`stats-${id}`).innerText =
        `Current: ${data.current_streak} Max: ${data.max_streak}`;
};

window.viewSkills = async function () {
    const data = await getSkills(localStorage.getItem("token"));

    const list = document.getElementById("skills-list");
    list.innerHTML = "";

    for (const skill of data) {
        const li = document.createElement("li");

        li.innerHTML = `
            <input id="skill-name-${skill.id}" value="${skill.name}" />
            <button onclick="addLog(${skill.id})">+</button>
            <button onclick="patchSkill(${skill.id})">Save</button>
            <button onclick="deleteSkill(${skill.id})">Delete</button>
            <div id="stats-${skill.id}"></div>
        `;

        list.appendChild(li);

        const stats = await getStats(skill.id, localStorage.getItem("token"));
        console.log(stats);

        document.getElementById(`stats-${skill.id}`).innerText =
            `Current: ${stats.current_streak} Max: ${stats.max_streak}`;
    }
};