

document.addEventListener('DOMContentLoaded', async function () {
    try {
        const moduleHandleData = await import('./handleData.js');
        const moduleHandleHTML = await import('./handleHTML.js');


        const statusData = await moduleHandleData.getAllStatus(); // Fetch all status data
        const robotList = await moduleHandleData.getRobotList(); // Fetch the robot list
        console.log('reponse', {statusData, robotList});

        if(robotList && Array.isArray(robotList)) {
            for(const robot of robotList){
                
                moduleHandleHTML.handleRobotList(robot[0], robot[1], robot[3]);
            }
        }


        /**
         * 
         * Add event listener for form submission
         * 
         */
        const formCreateRobot = document.getElementById("addRobotFormContainer");
        formCreateRobot.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const robotName = document.getElementById("robotName").value;
            const robotMission = document.getElementById("robotMission").value;

            try {
                const {uuid} = await moduleHandleData.createRobot(robotName, robotMission);
                console.log('Robot created:', uuid);

                if (!uuid) {
                    throw new Error('Robot creation failed, no UUID returned');
                }

                // Add the new robot to the UI 
                moduleHandleHTML.handleRobotList(uuid, robotName, robotMission);
                // Optionally, you can update the UI or show a success message here
            } catch (error) {
                console.error('Error creating robot:', error);
                // Optionally, you can show an error message to the user here
            }
        });


        

    } catch (error) {
        console.error('Error al importar el módulo:', error);
    }
});