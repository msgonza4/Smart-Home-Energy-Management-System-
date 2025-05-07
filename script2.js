document.getElementById("turn-on").addEventListener("click", () => {
    fetch("/control-appliance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ appliance: "Lamp", action: "on" })
    });
});

document.getElementById("turn-off").addEventListener("click", () => {
    fetch("/control-appliance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ appliance: "Lamp", action: "off" })
    });
});
