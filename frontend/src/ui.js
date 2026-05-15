export function showToast(message) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}

export function confirmAction(message) {
    return new Promise((resolve) => {
        const modal = document.getElementById("confirm-modal");
        const text = document.getElementById("confirm-text");
        const yes = document.getElementById("confirm-yes");
        const no = document.getElementById("confirm-no");

        text.innerText = message;
        modal.classList.remove("hidden");

        yes.onclick = () => {
            modal.classList.add("hidden");
            resolve(true);
        };

        no.onclick = () => {
            modal.classList.add("hidden");
            resolve(false);
        };
    });
}
