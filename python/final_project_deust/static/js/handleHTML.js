

export function handleRobotList(id, nom, mission){

    const row = `
        <tr data-robotId="${id}">
            <td class="td_robot_list" data-robotId="${id}">${id.slice(10)+"..."}</td>
            <td class="td_robot_list">${nom}</td>
            <td class="td_robot_list">${mission}</td>
            <td class="td_robot_list">
                <button type="button" data-robotId="${id}" class="btn-effacer">Effacer</button>
            </td>
        </tr>
    `;

    const tableBody = document.getElementById("robotListBody");
    if (tableBody) {
        tableBody.insertAdjacentHTML('beforeend', row);
    } else {
        console.error("Table body with id 'robotListBody' not found.");
    }

    /**
     * 
     * Handle delete button click
     * 
    **/
    const btnDelete = document.querySelector(".btn-effacer data-robotID='"+id+"'"); // Usamos querySelector en newRow
    //todo: trabajar en el boton borrar
    if(btnDelete){
        btnDelete.addEventListener("click", async function(event){
            const robotId = event.target.getAttribute("data-robotId");
            console.log("Effacer le robot avec l'ID:", robotId);
            // Aquí podrías añadir la lógica para eliminar la fila del DOM
            // y hacer la llamada a la API para eliminar el robot
        });
    }
}