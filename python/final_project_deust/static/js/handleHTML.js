export function handleRobotList(id, nom, mission) {
    const tableBody = document.getElementById("robotListBody");
    if (!tableBody) {
        console.error("Table body with id 'robotListBody' not found.");
        return;
    }

    const row = document.createElement("tr");
    row.dataset.robotId = id;

    row.innerHTML = `
        <td class="td_robot_list">${id.slice(0,15)}...</td>
        <td class="td_robot_list">${nom}</td>
        <td class="td_robot_list">${mission}</td>
        <td class="td_robot_list">
            <button type="button" data-robot-id="${id}" class="btn-effacer">Effacer</button>
        </td>
    `;

    tableBody.appendChild(row);
}


// This function allow me to add the options in the select box with robot id
export function handleRobotListForSelectBox(id, nom){
    const selectBox = document.getElementById("robotNameSelectBox");
    if (!selectBox) {
        console.error("Select box with id 'robotName' not found.");
        return;
    }
    const option = ` <option value="${id}" style="font-size: 1rem;">${nom}</option>`
    selectBox.insertAdjacentHTML("beforeend", option);
}


// Asignar el manejador de eventos una sola vez (event delegation)
document.addEventListener("DOMContentLoaded", async() => {

    const moduleHandleData = await import('./handleData.js');

    const tableBody = document.getElementById("robotListBody");
    if (!tableBody) return;

    tableBody.addEventListener("click", async function (event) {
        const btn = event.target.closest(".btn-effacer");
        if (!btn) return;

        const robotId = btn.getAttribute("data-robot-id");
        if (!robotId) {
            console.error("Robot ID not found in button data attribute.");
            alert("On a pas pu trouver l'ID du robot à supprimer.");
            return;
        }
        try {
            const delete_Reponse = await moduleHandleData.deleteRobot(robotId);

            if(delete_Reponse.message !== "robot supprimé") {
                throw new Error("Failed to delete robot");
            }

            // Eliminar fila del DOM
            const row = btn.closest("tr");
            if (row) row.remove();

            // delete the instruction associated with the robot id
            const reponse_deleteInstruction = await moduleHandleData.deleteInstruction(robotId);
            if (reponse_deleteInstruction.message !== "Instruction supprimée avec succès") {
                throw new Error("Failed to delete instruction");
            }

            // delete the option in the select box that match the robot id
            const selectBox = document.getElementById("robotNameSelectBox");
            if (selectBox) {
                const optionToRemove = selectBox.querySelector(`option[value="${robotId}"]`);
                if (optionToRemove) {
                    optionToRemove.remove();
                }
            }

        } catch (error) {
            console.error("Error al eliminar el robot:", error);
            alert("Erreur lors de la suppression du robot. Veuillez réessayer.");
        }
    });
});


// This function allow to show the status of each robot in the UI
export function handleStatusList(nom, date, lignes, cubes = 3,status) {
    const tableBody = document.getElementById("robotStatusBody");
    if (!tableBody) {
        console.error("Table body with id 'statusListBody' not found.");
        return;
    }

    const row = `
        <tr>
            <td style="width: 25%;text-align: start;height:3rem;border-bottom: 1px solid #f0f0f0;";">${nom}</td>
            <td style="width: 25%;text-align: start;height:3rem;border-bottom: 1px solid #f0f0f0;";">${date}</td>
            <td style="width: 25%;text-align: start;height:3rem;border-bottom: 1px solid #f0f0f0;";">${lignes}</td>
            <td style="width: 25%;text-align: start;height:3rem;border-bottom: 1px solid #f0f0f0;";">${cubes}</td>
            <td style="width: 25%;text-align: start;height:3rem;border-bottom: 1px solid #f0f0f0;";">${status}</td>
        </tr>
    `;

    tableBody.insertAdjacentHTML("beforeend", row);
}
