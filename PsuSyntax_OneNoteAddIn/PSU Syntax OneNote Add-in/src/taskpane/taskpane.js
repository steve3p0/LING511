/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office */

const HOST = "https://fd6a814d.ngrok.io"

Office.onReady(info =>
{
    if (info.host === Office.HostType.OneNote)
    {
        document.getElementById("sideload-msg").style.display = "none";
        document.getElementById("app-body").style.display = "flex";
        document.getElementById("run").onclick = run;
    }
});

export async function run()
{
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

                        addOutlineToPage(html);
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

// Add a table that displays the final grade, individual scores, and comments to the page.
function addOutlineToPage(html) {
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

function createHtmlParseTable(data)
{
    const sentence = data["sentence"];
    const parser = data["parser"];
    const formats = data["response_formats"];

    const byteImageTree = formats["tree_image"];
    const asciiTree = formats["tree_ascii"].replace(/\n/g, "<br />");
    const bracketDiagram = formats["bracket_diagram"];
    const parseStr = formats["tree_str"];

    // Build html img to hold Byte array image
    // <img src='name:image-block-name' alt='a cool image' width='500'/>
    var html_byteImageTree =
        //"<img src='name:image-block-name' alt='" + sentence + "' width='500'/>"
        //"<img src='name:image-block-name' alt='" + sentence + "' width='500'/>"
        "<img src='data:image/jpeg;base64," + byteImageTree + "' alt='" + sentence + "' width='500'/>";

    // Build html span for ASCII Tree
    var html_asciiTree =
        "<span style='font-family: Courier New'>"
        + "<pre>"
        + asciiTree
        + "</pre>"
        + "</span>";

    //var html_asciiTree = html_asciiTree_before.replace(/ /g, '\u00a0');
    //const nbsp = "&nbsp"

    var exampleBracketDiagram = "[<sub>TP</sub> [<sub>NP</sub> [<sub>N</sub> boy]] [<sub>VP</sub> [<sub>V</sub> meets] [<sub>NP</sub> [<sub>N</sub> world]]]]"

    var htmlBracketDiagram = subscriptParseTagsInHtml(bracketDiagram);

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

        // Syntax Tree (Image): PNG image embedded into an <img> tag as a byte string
        + "<tr><td>"
        + "<b>Syntax Tree (Image)</b>"
        + "</td></tr>"
        + "<tr><td>"
        +  html_byteImageTree
        + "</td></tr>"

        // Syntax Tree (ASCII) Format: Pretty Printed ASCII Art
        + "<tr><td>"
        + "<b>Syntax Tree (ASCII)</b>"
        + "</td></tr>"
        + "<tr><td>"
        +  html_asciiTree
        + "</td></tr>"

        // Bracketed Diagram: otherwise known as "Labelled Bracketing"
        + "<tr bgcolor='#d3d3d3'><td>"
        + "<b>Bracket Diagram</b>"
        + "</td></tr>"
        + "<tr><td>"
        + htmlBracketDiagram
        // + exampleBracketDiagram
        + "</td></tr>"

        // Parse String: Similary to Bracket Diagram but uses () instead of []
        + "<tr bgcolor='#d3d3d3'><td>"
        + "<b>Parse String</b>"
        + "</td></tr>"
        + "<tr><td>"
        + parseStr
        + "</td></tr>"

        + "</table>";

    return html
}


function subscriptParseTagsInHtml(bracketDiagram)
{
    // var exampleBracketDiagram = "[<sub>TP</sub> [<sub>NP</sub> [<sub>N</sub> boy]] [<sub>VP</sub> [<sub>V</sub> meets] [<sub>NP</sub> [<sub>N</sub> world]]]]";
    // var bracketDiagram = "[TP [NP [N boy]] [VP [V meets] [NP [N world]]]]";

    var re = /(?<=\[)(\w+)/gi;
    var subBracket = bracketDiagram.replace(re, "<sub>$1</sub>");

    //console.log(walkNest()); // returned nest array  [0, 1, 1, 1, 2, 2, 1, 0]

    // Create newText by appendening parse tree
    var html = ""
        // Bracketed Diagram: otherwise known as "Labelled Bracketing"
        //+ exampleBracketDiagram;
        + subBracket;

    return html
}


function createHtmlParseTable2(data)
{
    const sentence = data["sentence"];
    const parser = data["parser"];
    const formats = data["response_formats"];

    //const bracketDiagram = formats["bracket_diagram"];

    var exampleBracketDiagram = "[<sub>TP</sub> [<sub>NP</sub> [<sub>N</sub> boy]] [<sub>VP</sub> [<sub>V</sub> meets] [<sub>NP</sub> [<sub>N</sub> world]]]]";

    var bracketDiagram = "[TP [NP [N boy]] [VP [V meets] [NP [N world]]]]";

    //var matchBracket = new RegExp("(?<=\\[)(\\w+)")
    //var subBracket = bracketDiagram.replace(matchBracket, "<sub>$&</sub>")

    //var bracketDiagram = '<img src="[media id=5]" />';
    var re = /(?<=\[)(\w+)/gi;
    var subBracket = bracketDiagram.replace(re, "<sub>$1</sub>");

    //console.log(walkNest()); // returned nest array  [0, 1, 1, 1, 2, 2, 1, 0]

    // Create newText by appendening parse tree
    var html = ""
        // Bracketed Diagram: otherwise known as "Labelled Bracketing"
        //+ exampleBracketDiagram;
        + subBracket;

    return html
}

//var strg = '{  {  }  {  {  }  }  }'; // basic nest
var strg = '{TP {NP {N boy}} {VP {V meets} {NP {N world}}}}'
var brakRX = /[}|{]/g; // simple match for { or }
var nest = [];

function walkNest(lvl, found)
{
    found = found || brakRX.exec(strg);

    if (found == '{')
    {
        lvl = (lvl == undefined) ? 0 : lvl + 1;
        nest.push(lvl);
        walkNest(lvl);
    }
    else if (found == '}')
    {
        return;
    }
    // '}' base condition met. returning stack

    // check next character before returning.
    nest.push(lvl);
    if (brakRX.exec(strg) == '{')
    {
        walkNest(lvl-1, '{');
    }
    return nest;

}


// function walkNest(lvl, found)
// {
//     found = found || brakRX.exec(strg);
//
//     if (found == '{')
//     {
//         lvl = (lvl == undefined) ? 0 : lvl + 1;
//         nest.push(lvl);
//         walkNest(lvl);
//     }
//     else if (found == '}')
//     {
//         return;
//     }
//     // '}' base condition met. returning stack
//
//     // check next character before returning.
//     nest.push(lvl);
//     if (brakRX.exec(strg) == '{')
//     {
//         walkNest(lvl-1, '{');
//     }
//     return nest;
//
// }


// function colorNestedBrackets(block)
// {
//     // var block = /* code block */
//     var startIndex = 0; /* index of first bracket */
//
//     var currPos = startIndex;
//     var openBrackets = 0;
//     var stillSearching = true;
//     var waitForChar = false;
//
//     while (stillSearching && currPos <= block.length) {
//         var currChar = block.charAt(currPos);
//
//         if (!waitForChar) {
//             switch (currChar) {
//                 case '{':
//                     openBrackets++;
//                     break;
//                 case '}':
//                     openBrackets--;
//                     break;
//                 case '"':
//                 case "'":
//                     waitForChar = currChar;
//                     break;
//                 case '/':
//                     var nextChar = block.charAt(currPos + 1);
//                     if (nextChar === '/') {
//                         waitForChar = '\n';
//                     } else if (nextChar === '*') {
//                         waitForChar = '*/';
//                     }
//             }
//         } else {
//             if (currChar === waitForChar) {
//                 if (waitForChar === '"' || waitForChar === "'") {
//                     block.charAt(currPos - 1) !== '\\' && (waitForChar = false);
//                 } else {
//                     waitForChar = false;
//                 }
//             } else if (currChar === '*') {
//                 block.charAt(currPos + 1) === '/' && (waitForChar = false);
//             }
//         }
//
//         currPos++
//         if (openBrackets === 0) { stillSearching = false; }
//     }
//
//     console.log(block.substring(startIndex , currPos)); // contents of the outermost brackets incl. everything inside
// }