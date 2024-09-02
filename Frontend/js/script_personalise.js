        // Temporary user ID generation (for demonstration purposes)
        const temporaryUserId = 'user_' + Math.floor(Math.random() * 1000000);

        function formatItineraryText(text) {
            // Replace text between asterisks with bold text
            const formattedText = text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
        
            // Insert new lines where there are line breaks in the original text
            const formattedWithNewLines = formattedText.replace(/\n/g, '<br>');
        
            return formattedWithNewLines;
        }


        document.getElementById('itineraryForm').addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            // Collect form data
            const days = document.getElementById('days').value;
            const price = document.getElementById('price').value;
            const categories = Array.from(document.querySelectorAll('input[name="categories"]:checked'))
                .map(cb => cb.value);

            // Validate that at least one category is selected
            if (categories.length < 1) {
                alert('Please select at least one interest category.');
                return;
            }

            // Prepare data object to send to the server
            const requestData = {
                Days: parseInt(days),
                Price: price,
                Categories: categories,
            };

            // Send data to the Heroku deployment's /predict endpoint
            fetch('https://knnfirst-a4ea992f23e1.herokuapp.com/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {


                        
                        const itineraryText=`Predicted Cluster: ${data.prediction}`;;

                        const formattedItinerary = formatItineraryText(itineraryText);
                        // document.getElementById('itineraryResponse').textContent =formattedItinerary;



                        document.getElementById('itineraryResponse').textContent = formattedItinerary;
                        // Display the response
                        document.getElementById('responseContainer').style.display = 'block'; // Show the response container with buttons
                    }
                })
                .catch(error => {
                    alert('An error occurred while processing your request.');
                    console.error('Error:', error);
                });
        });

        // Handling the "Itinerary OK" button click
        document.getElementById('itinerary-ok').addEventListener('click', function () {
            const itineraryData = {
                Days: parseInt(document.getElementById('days').value),
                Price: document.getElementById('price').value,
                Categories: Array.from(document.querySelectorAll('input[name="categories"]:checked'))
                    .map(cb => cb.value),
                Itinerary: document.getElementById('itineraryResponse').textContent,
                UserId: temporaryUserId // Using the temporary user ID
            };

            // Save the itinerary with the user ID
            fetch('https://knnfirst-a4ea992f23e1.herokuapp.com/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(itineraryData)
            })
                .then(response => response.json())
                .then(data => {
                    alert('Itinerary saved successfully with ID: ' + data.inserted_id);
                })
                .catch(error => {
                    alert('An error occurred while saving the itinerary.');
                    console.error('Error:', error);
                });
        });


        // Handling the "Not Suitable" button click
        // document.getElementById('not-suitable').addEventListener('click', function () {
        //     const days = document.getElementById('days').value;
        //     const price = document.getElementById('price').value;
        //     const categories = Array.from(document.querySelectorAll('input[name="categories"]:checked'))
        //         .map(cb => cb.value);

        //     const requestData = {
        //         duration: parseInt(days),
        //         budget: price,
        //         interests: categories

        //     }
        // });

        //     // Send data to the Heroku deployment's /generate_itinerary endpoint
        //     fetch('https://shielded-chamber-62491-e124d88dd0d7.herokuapp.com/generate_itinerary', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'
        //         },
        //         body: JSON.stringify(requestData)
        //     })
        //         .then(response => response.json())
        //         .then(data => {
        //             if (data.error) {
        //                 alert(data.error);
        //             } else {
        //                 console.log("Creating a new itenarary...");
        //                 document.getElementById('itineraryResponse').textContent = `Generated Itinerary: ${data.Itinerary}`; // Display the new itinerary
        //                 document.getElementById('responseContainer').style.display = 'block'; // Show the response container with buttons
        //             }
        //         })
        //         .catch(error => {
        //             alert('An error occurred while generating an alternative itinerary.');
        //             console.error('Error:', error);
        //         });
        // });



        document.getElementById('not-suitable').addEventListener('click', function () {
            const days = document.getElementById('days').value;
            const price = document.getElementById('price').value;
            const categories = Array.from(document.querySelectorAll('input[name="categories"]:checked'))
                .map(cb => cb.value);

            const requestDataForGenerate = {
                duration: parseInt(days),
                budget: price,
                interests: categories
            };

            const fullRequestData = {
                requestData: requestDataForGenerate,
                userId: temporaryUserId  // Pass the temporary user ID
            };

            // Send data to the Heroku deployment's /generate_itinerary endpoint
            fetch('https://shielded-chamber-62491-e124d88dd0d7.herokuapp.com/generate_itinerary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(fullRequestData)  // Pass the structured request data
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        console.log("Creating a new itinerary...");
                        const itineraryText=`Generated Itinerary: ${data.Itinerary}`;

                        const formattedItinerary = formatItineraryText(itineraryText);
                        document.getElementById('itineraryResponse').textContent =formattedItinerary; // Display the new itinerary
                        document.getElementById('responseContainer').style.display = 'block'; // Show the response container with buttons
                    }
                })
                .catch(error => {
                    alert('An error occurred while generating an alternative itinerary.');
                    console.error('Error:', error);
                });
        });


