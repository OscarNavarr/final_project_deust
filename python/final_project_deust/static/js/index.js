document.addEventListener('DOMContentLoaded', async function () {
    try {
        const moduleHandleData = await import('./handleData.js');
        const moduleHandleHTML = await import('./handleHTML.js');
        const moduleHandleCharts = await import('./handlecharts.js');

        const statusData = await moduleHandleData.getAllStatus(); // Fetch all status data
        const allInstructions = await moduleHandleData.getAllInstructionList(); // Fetch all instructions
        const robotList = await moduleHandleData.getRobotList(); // Fetch the robot list


        console.log('reponse', {statusData, robotList});
        console.log('allInstructions', allInstructions);

        if(robotList && Array.isArray(robotList)) {
            for(const robot of robotList){
                
                moduleHandleHTML.handleRobotList(robot[0], robot[2], robot[4]);
            }
        }

        /**
         * Show all instructions in the UI
         */
        for(const instruction of allInstructions){
            moduleHandleHTML.handleInstructionList(instruction.instruction_id, instruction.robot_id, instruction.robot_name, instruction.instruction, instruction.recovered_robot); 
        }

        moduleHandleCharts.handleBarChart(allInstructions); // Call the function to handle the bar chart


        /**
         * 
         * Add event listener for form submission to create robot 
         * 
         */
        const formCreateRobot = document.getElementById("addRobotFormContainer");
        formCreateRobot.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const robotName = document.getElementById("robotName").value;
            const robotUUID = document.getElementById("uuid_robot").value;
            const robotMission = document.getElementById("robotMission").value;

            try {
                if (!robotName || !robotMission || !robotUUID) {
                    throw new Error('All fields are required to create a robot');
                }
                const {uuid} = await moduleHandleData.createRobot(robotName, robotUUID, robotMission);
                console.log('Robot created:', uuid);

                if (!uuid) {
                    throw new Error('Robot creation failed, no UUID returned');
                }

                // Add the new robot to the UI 
                moduleHandleHTML.handleRobotList(uuid, robotName, robotMission);
                // Add the new robot to the select box for instructions
                moduleHandleHTML.handleRobotListForSelectBox(uuid, robotName);

                // reset the form fields after successful creation
                document.getElementById("robotName").value = '';
                document.getElementById("uuid_robot").value = '';



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
            const robotName = document.getElementById("robotNameSelectBox").options[document.getElementById("robotNameSelectBox").selectedIndex].text;
            const instruction = document.getElementById("instructionType").value; // return String: "1,2,4,6,..."
           
            try {
                if (!robotId || !instruction) {
                    throw new Error('Robot ID and instruction are required');
                }

                const response = await moduleHandleData.createInstruction(robotId, instruction);
                console.log('Instruction created:', response);

                document.getElementById("instructionType").value = ''; // Reset the instruction input field
                
                // Add the new instruction to the UI  
                moduleHandleHTML.handleInstructionList(response.instruction_id, 0, robotName, instruction, 0);

                alert('Instruction créée avec succès !');
            } catch (error) {
                alert('Erreur lors de la création de l\'instruction : ' + error.message);
                console.error('Error creating instruction:', error);
            }
        })
        
        /**
         * Get all status and update the UI
         */
        for(const status of statusData){
            moduleHandleHTML.handleStatusList(status[0], status[2], status[3], status[4]);
        }
    } catch (error) {
        console.error('Error al importar el módulo:', error);
    }
});