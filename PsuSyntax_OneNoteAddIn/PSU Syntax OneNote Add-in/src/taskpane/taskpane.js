/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office */

Office.onReady(info =>
{
    if (info.host === Office.HostType.OneNote)
    {
        document.getElementById("sideload-msg").style.display = "none";
        document.getElementById("app-body").style.display = "flex";
        document.getElementById("run").onclick = run;
    }
});

export async function run() {
    /**
     * Insert your OneNote code here
     */

    try
    {
        // eslint-disable-next-line no-undef
        await OneNote.run(async context =>
        {

            // Get the current page.
            var page = context.application.getActivePage();

            // Queue a command to set the page title.
            page.title = "STRING PARSED";

            // // Queue a command to add an outline to the page.
            // var html = "<p><ol><li>Item #1</li><li>Item #2</li></ol></p>";
            // page.addOutline(40, 90, html);


            Office.context.document.getSelectedDataAsync(Office.CoercionType.Text, function (asyncResult)
            {
                if (asyncResult.status == Office.AsyncResultStatus.Failed)
                {
                    write('Action failed. Error: ' + asyncResult.error.message);
                }
                else
                {
                    //write('Selected data: ' + asyncResult.value);

                    var selectedText = asyncResult.value
                    var parseStr = "";

                    const host = "https://47abd88d.ngrok.io"
                    const axios = require('axios').default;
                    axios.post(host + '/parse',
                    {
                        sentence: selectedText
                    })
                    .then(function (response)
                    {
                        parseStr = response.data;
                        // Create newText by appendening parse tree
                        var newText = selectedText
                            + "<br><br>"
                            + "Parse String: <br>"
                            + parseStr ;
                        console.log("New text is: " + newText);

                        // Replace selected text with newText value.
                        Office.context.document.setSelectedDataAsync(newText, { coercionType: "html" },
                            function (asyncResult) {
                                var error = asyncResult.error;
                                if (asyncResult.status === Office.AsyncResultStatus.Failed) {
                                    console.log(error.name + ": " + error.message);
                                }
                            });

                        console.log(response);
                    })
                    .catch(function (error)
                    {
                        console.log(error);
                    });


                    // // Queue a command to add an outline to the page.
                    // var html = "<p><ol>"
                    //     + "<li>Sentence: " + selectedText + "</li>"
                    //     + "<li>Parse Tree: " + parseStr + "</li></ol></p>";
                    // page.addOutline(40, 90, html);

                }
            });

            // Run the queued commands, and return a promise to indicate task completion.
            return context.sync();
        });
    }
    catch (error)
    {
        // eslint-disable-next-line no-undef
        console.log("Error: " + error);
    }
}

// function getSelectedText()
// {
//     var selected = ""
//     Office.context.document.getSelectedDataAsync(Office.CoercionType.Text, function (asyncResult)
//     {
//         if (asyncResult.status == Office.AsyncResultStatus.Failed)
//         {
//             write('Action failed. Error: ' + asyncResult.error.message);
//         }
//         else
//         {
//             //write('Selected data: ' + asyncResult.value);
//
//             selected = asyncResult.value;
//         }
//     });
//
//     return selected;
// }

// Function that writes to a div with id='message' on the page.
function write(message)
{
    document.getElementById('message').innerText += message;
}


// function getSelectedText() {
//     Office.context.document.getSelectedDataAsync(Office.CoercionType.Text,
//         { valueFormat: "unformatted" },
//         function (asyncResult) {
//             var error = asyncResult.error;
//             if (asyncResult.status === Office.AsyncResultStatus.Failed) {
//                 console.log(error.name + ": " + error.message);
//             }
//             else {
//                 // Get selected data.
//                 var dataValue = asyncResult.value;
//                 console.log("Selected data is: " + dataValue);
//
//                 return dataValue;
//             }
//         });
// }

