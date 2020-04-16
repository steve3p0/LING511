/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office */

Office.onReady(info => {
  if (info.host === Office.HostType.OneNote) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = run;
  }
});

export async function run() {
  /**
   * Insert your OneNote code here
   */

  try {
    await OneNote.run(async context => {

      // Get the current page.
      var page = context.application.getActivePage();

      // Queue a command to set the page title.
      page.title = "Hello World";

      // Queue a command to add an outline to the page.
      var html = "<p><ol><li>Item #1</li><li>Item #2</li></ol></p>";
      page.addOutline(40, 90, html);

      // Run the queued commands, and return a promise to indicate task completion.
      return context.sync();
    });
  } catch (error) {
    console.log("Error: " + error);
  }
}
