/**
 * Set the cookie for user id
 * @param cname
 * @param cvalue
 * @param exdays
 */

var UNIQUE_USER_ID = "uniqueUserIdentifier";

function copyStringToClipboard (str) {
    showButton(false);
    console.log("copyStringToClipboard : ready to copy" + str);
    document.getElementById("okButton").addEventListener("click", function(){
       // Create new element
       var el = document.createElement('textarea');
       // Set value (string to be copied)
       el.value = str;
       // Set non-editable to avoid focus and move outside of view
       document.body.appendChild(el);
       // Select text inside element
       el.select();
       // Copy text to clipboard
       document.execCommand('copy');
       // Remove temporary element
       document.body.removeChild(el);
       console.log("copyStringToClipboard : success")
       showButton(true);
       paste();
    });
}

function showButton(value)   {
    console.log('showButton : ' + value);
    if(value)   {
        document.getElementById("okButton").style.visibility = "hidden";
        document.getElementById("contButton").style.visibility = "visible";
    }else   {
        document.getElementById("contButton").style.visibility = "hidden";
        document.getElementById("okButton").style.visibility = "visible";
    }
}

function paste() {
  console.log("paste: pasting...");
  var pasteText = document.querySelector("#output");
  pasteText.focus();
  document.execCommand('paste');
  console.log(pasteText.textContent);
  console.log("paste: success");
}