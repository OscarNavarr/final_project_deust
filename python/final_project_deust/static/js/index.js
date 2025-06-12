

document.addEventListener('DOMContentLoaded', async function () {
    try {
        const moduleHandleData = await import('./handleData.js');
        const moduleHandleHTML = await import('./handleHTML.js');


        const statusData = await moduleHandleData.getAllStatus(); // Fetch all status data
        const robotList = await moduleHandleData.getRobotList(); // Fetch the robot list
        console.log('reponse', {statusData, robotList});

        if(robotList && Array.isArray(robotList)) {
            for(const robot of robotList){
                
                moduleHandleHTML.handleRobotList(robot[0], robot[2], robot[4]);
            }
        }


        /**
         * 
         * Add event listener for form submission to create robot 
         * 
         */
        const formCreateRobot = document.getElementById("addRobotFormContainer");
        formCreateRobot.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const robotName = document.getElementById("robotName").value;
            const robotAddressMac = document.getElementById("addresseMac").value;
            const robotMission = document.getElementById("robotMission").value;

            try {
                if (!robotName || !robotMission || !robotAddressMac) {
                    throw new Error('All fields are required to create a robot');
                }
                const {uuid} = await moduleHandleData.createRobot(robotName, robotAddressMac, robotMission);
                console.log('Robot created:', uuid);

                if (!uuid) {
                    throw new Error('Robot creation failed, no UUID returned');
                }

                // Add the new robot to the UI 
                moduleHandleHTML.handleRobotList(uuid, robotName, robotMission);
                // Add the new robot to the select box for instructions
                moduleHandleHTML.handleRobotListForSelectBox(uuid, robotName);
            } catch (error) {
                console.error('Error creating robot:', error);
                // Optionally, you can show an error message to the user here
            }
        });


        /**
         * Get all robot name and put them in the select box for add instruction
        **/
        for(const robot of robotList){
            moduleHandleHTML.handleRobotListForSelectBox(robot[0], robot[2]);
        }

        /**
         * Handle form to create instruction
         */
        const addInstructionsForm = document.getElementById("addInstructionsForm");
        addInstructionsForm.addEventListener("submit", async function(event) {
            event.preventDefault(); // Prevent the default form submission

            const robotId = document.getElementById("robotNameSelectBox").value;
            const instruction = document.getElementById("instructionType").value; // return String: "1,2,4,6,..."
           
            try {
                if (!robotId || !instruction) {
                    throw new Error('Robot ID and instruction are required');
                }

                const response = await moduleHandleData.createInstruction(robotId, instruction);
                console.log('Instruction created:', response);

                // Update the UI or show a success message here
            } catch (error) {
                alert('Erreur lors de la création de l\'instruction : ' + error.message);
                console.error('Error creating instruction:', error);
            }
        })
        
        /**
         * Get all status and update the UI
         */
        for(const status of statusData){
            moduleHandleHTML.handleStatusList(status[0], status[2], status[3], 4, status[4]);
        }
    } catch (error) {
        console.error('Error al importar el módulo:', error);
    }
});