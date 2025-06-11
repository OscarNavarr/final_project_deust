export async function getAllStatus(){
    try {
        
        const response = await fetch('/all_status');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data; // Return the fetched data for further processing

    } catch (error) {
        console.error("Error fetching data:", error);
        throw error; // Re-throw the error for further handling if needed
    }
}

export async function getRobotList(){
    try {
        const reponse = await fetch('/robots');
        if (!reponse.ok) {
            throw new Error(`HTTP error! status: ${reponse.status}`);
        }
        const data = await reponse.json();
        return data; // Return the fetched robot list for further processing

    } catch (error) {
        console.error("Error fetching robot list:", error);
        throw error; // Re-throw the error for further handling if needed
        
    }
}

export async function createRobot(robotName, robotAddressMac, robotMission){
    try {
        const response = await fetch('/robot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: robotName, addressMac: robotAddressMac, mission: robotMission })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data; // Return the created robot id for further processing
    } catch (error) {
        console.error("Error creating robot:", error);
        throw error; // Re-throw the error for further handling if needed
    }
}

export async function deleteRobot(robotId){
    try {
        
        const reponse = await fetch(`/delete_robot/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ robot_id: robotId })
        })

        if (!reponse.ok) {
            throw new Error(`HTTP error! status: ${reponse.status}`);
        }
        const data = await reponse.json();

        return data; // Return the response data for further processing
    } catch (error) {
        console.error("Error deleting robot:", error);
        throw error; // Re-throw the error for further handling if needed
    }
}

export async function createInstruction(robotId, instructionValue){
    try {
        const response = await fetch('/create_instruction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ robot_id: robotId, instruction: instructionValue })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data; // Return the created instruction id for further processing
    } catch (error) {
        console.error("Error creating instruction:", error);
        throw error; // Re-throw the error for further handling if needed
    }
}


export async function deleteInstruction(robotId){
    try {
        
        const response = await fetch(`/delete_instruction/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ robot_id: robotId })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data; // Return the response data for further processing

    } catch (error) {
        console.error("Error deleting instruction:", error);
        throw error; // Re-throw the error for further handling if needed
    }
}