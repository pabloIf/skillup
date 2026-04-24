const API = "http://127.0.0.1:8000/api";

export async function login(username, password) {
    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    });

    const data = await res.json();
    console.log("LOGIN RESPONSE:", data);
    if (res.ok) {
        localStorage.setItem("token", data.access_token);
    } else {
        alert("Login failed");
    }
    
    return data;
}

export async function register(data) {
    const res = await fetch(`${API}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return await res.json();
}

export async function getSkills(token) {
    const res = await fetch(`${API}/skills`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    return await res.json();
}

export async function createSkill(name, token) {
    const res = await fetch(`${API}/skills`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name })
    });

    return await res.json();
}

export async function deleteSkill(id, token) {
    const res = await fetch(`${API}/skills/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    return await res.json();
}

export async function addLog(skillId, token) {
    const res = await fetch(`${API}/logs`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            skill_id: skillId,
            date: new Date().toISOString().split("T")[0]
        })
    });

    const result = await res.json();
    if (!res.ok) {
        throw new Error(result.detail || "Something went wrong");
    }

    return result;
}

export async function getStats(skillId, token) {
    const res = await fetch(`${API}/skills/${skillId}/stats`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    return await res.json();
}

export async function patchSkill(id, name, token) {
    const res = await fetch(`${API}/skills/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name })
    });

    return await res.json();
}