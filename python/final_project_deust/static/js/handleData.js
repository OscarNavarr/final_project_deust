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

export async function createRobot(robotName, robotMission){
    try {
        const response = await fetch('/robot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: robotName, mission: robotMission })
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