/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office */

const HOST = "https://7228f422.ngrok.io"

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

                    var request_formats = []
                    const ckb = document.querySelectorAll("#outputs input[type=checkbox]");
                    var checkedOne = Array.prototype.slice.call(ckb).some(x => x.checked);

                    if (!checkedOne)
                    {
                        // Then fuckoff
                        // You need to select at least one output format
                    }

                    [...ckb].forEach( el =>
                    {
                        if( el.checked )
                        {
                            // Is checked!
                            request_formats.push(el.id)
                            //data.append(el.name, True)
                            console.log( el.id )
                        }
                    });

                    //const parserType = document.querySelector('input[name="type"]:checked').value;
                    const parserType = document.querySelector('#types input[name="parser_type"]:checked').value;

                    var data = new FormData();
                    data.append("sentence", selectedText);
                    data.append("parser", parserType);
                    data.append("request_formats", JSON.stringify(outputs))

                    const axios = require('axios').default;

                    axios.post(HOST + '/parse',
                    {
                        sentence: selectedText,
                        parser: parserType,
                        request_formats: request_formats
                    })
                    .then(function (response)
                    {
                        const response_data = response.data;
                        console.log(response);

                        var html = createHtmlParseTable(response_data);

                        addHOutlineToPage(html);
                        // Add an outline with the specified HTML to the page.
                        var outline = page.addOutline(560, 70, html);
                    })
                    .catch(function (error)
                    {
                        console.log(error);
                    });
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

// Function that writes to a div with id='message' on the page.
function write(message)
{
    document.getElementById('message').innerText += message;
}

function createHtmlParseTable(data)
{
    const sentence = data["sentence"];
    const parser = data["parser"];
    const formats = data["response_formats"];

    const asciiTree = formats["tree_ascii"].replace(/\n/g, "<br />");
    const bracketDiagram = formats["bracket_diagram"];
    const parseStr = formats["tree_str"];

    // const html_asciiTree =
    //     "<span style='font-family: Courier New'>"
    //     + "<p>"
    //     + asciiTree
    //     + "</p>"
    //     + " </span>";


    // Build html span for ASCII Tree
    var html_asciiTree =
        "<span style='font-family: Courier New'>"
        + "<pre>"
        + asciiTree
        + "</pre>"
        + "</span>";

    //var html_asciiTree = html_asciiTree_before.replace(/ /g, '\u00a0');

    //const nbsp = "&nbsp"

    // const html_asciiTree =
    //     "<p>"
    //     + response_asciiTree
    //     + "</p>";

    var exampleBracketDiagram = "[<sub>TP</sub> [<sub>NP</sub> [<sub>N</sub> boy]] [<sub>VP</sub> [<sub>V</sub> meets] [<sub>NP</sub> [<sub>N</sub> world]]]]"

    // Create newText by appendening parse tree
    var html = ""
        // CSS Note working?
        + "<table border=1>"
        //+ "<table border=3D1 cellpadding=3D0 cellspacing=3D0 valign=3Dtop "
        //    + "style=3D'direction:ltr;border-collapse:collapse;border-style:solid;border-color:#A3A3A3;border-width: 1pt' title=3D'' summary=3D''>"
        //+ "<table class='pdx-ling_parseTable'>"
        //+ "<tr bgcolor='#d3d3d3'><td>"
        //+ "<tr style='background-color: lightgray'><td>"
        //+ "<tr><td>"
        //+ "<tr bgcolor='#d3d3d3'><td>"
        //+ "<tr style='background-color: lightgray'><td>"
        //+ "<tr><td bgcolor='#d3d3d3'>"
        //+ "<tr><td style='background-color: lightgray'>"
        //+ "<tr><td style=3D'border-style:solid;border-color:#A3A3A3;border-width:1pt;background-color:#D8D8D8;vertical-align:top;width:3.8in;padding:2.0pt 3.0pt 2.0pt 3.0pt'>"
        + "<tr><td>"
        + "<b>Syntax Tree (ASCII)</b>"
        + "</td></tr>"
        + "<tr><td>"
        +  html_asciiTree
        + "</td></tr>"
        + "<tr bgcolor='#d3d3d3'><td>"
        + "<b>Bracket Diagram</b>"
        + "</td></tr>"
        + "<tr><td>"
        + bracketDiagram
        // + exampleBracketDiagram
        + "</td></tr>"
        + "<tr bgcolor='#d3d3d3'><td>"
        + "<b>Parse String</b>"
        + "</td></tr>"
        + "<tr><td>"
        + parseStr
        + "</td></tr>"
        + "</table>"

    // // Create newText by appendening parse tree
    // var newText = selectedText + table


    // // Create newText by appendening parse tree
    // var newText = selectedText
    // console.log("New text is: " + newText);
    //
    // // Replace selected text with newText value.
    // Office.context.document.setSelectedDataAsync(newText, { coercionType: "html" },
    //     function (asyncResult) {
    //         var error = asyncResult.error;
    //         if (asyncResult.status === Office.AsyncResultStatus.Failed) {
    //             console.log(error.name + ": " + error.message);
    //         }
    //     });

    return html
}

// Add a table that displays the final grade, individual scores, and comments to the page.
function addHOutlineToPage(html) {
    OneNote.run(function (context) {

        // Get the current page.
        var page = context.application.getActivePage();

        // Add an outline with the specified HTML to the page.
        var outline = page.addOutline(300, 70, html);

        // Run the queued commands, and return a promise to indicate task completion.
        return context.sync()
            .catch(function(error) {
                onError(error);
            });
    });
}
